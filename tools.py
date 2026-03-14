from strands import tool


@tool
def estimar_costo_lambda(
    invocaciones: int,
    duracion_ms: float,
    memoria_mb: int,
) -> str:
    """Estima el costo mensual de AWS Lambda.

    Calcula el costo aproximado en USD basado en el modelo de precios de AWS Lambda,
    considerando el costo por solicitud y el costo por GB-segundo de cómputo.
    Incluye el free tier mensual (1M solicitudes y 400,000 GB-s).

    Args:
        invocaciones: Número total de invocaciones por mes.
        duracion_ms: Duración promedio de cada invocación en milisegundos.
        memoria_mb: Memoria asignada a la función en MB (128 a 10240).

    Returns:
        Resumen del costo estimado mensual con desglose de conceptos.
    """
    PRECIO_POR_MILLON_SOLICITUDES = 0.20
    PRECIO_POR_GB_SEGUNDO = 0.0000166667
    FREE_TIER_SOLICITUDES = 1_000_000
    FREE_TIER_GB_SEGUNDOS = 400_000

    duracion_s = duracion_ms / 1000
    gb = memoria_mb / 1024
    gb_segundos = invocaciones * duracion_s * gb

    solicitudes_facturables = max(0, invocaciones - FREE_TIER_SOLICITUDES)
    gb_s_facturables = max(0, gb_segundos - FREE_TIER_GB_SEGUNDOS)

    costo_solicitudes = (solicitudes_facturables / 1_000_000) * PRECIO_POR_MILLON_SOLICITUDES
    costo_computo = gb_s_facturables * PRECIO_POR_GB_SEGUNDO
    costo_total = costo_solicitudes + costo_computo

    return (
        f"Estimación de costo mensual para AWS Lambda:\n"
        f"  - Invocaciones:        {invocaciones:,}\n"
        f"  - Duración promedio:   {duracion_ms} ms\n"
        f"  - Memoria:             {memoria_mb} MB\n"
        f"  - GB-segundos totales: {gb_segundos:,.2f}\n"
        f"  - Costo solicitudes:   ${costo_solicitudes:.4f} USD\n"
        f"  - Costo cómputo:       ${costo_computo:.4f} USD\n"
        f"  - TOTAL ESTIMADO:      ${costo_total:.4f} USD/mes\n"
        f"  (Free tier aplicado: 1M solicitudes y 400,000 GB-s)"
    )


@tool
def recomendar_arquitectura(caso_de_uso: str) -> str:
    """Devuelve una arquitectura AWS recomendada según el caso de uso.

    Proporciona una recomendación de servicios AWS y el patrón arquitectónico
    más adecuado para cada tipo de aplicación o carga de trabajo.

    Args:
        caso_de_uso: Tipo de aplicación. Valores válidos:
            - "api_rest": API RESTful con backend serverless o contenedores.
            - "streaming": Procesamiento de datos en tiempo real.
            - "ml_inference": Inferencia de modelos de machine learning.
            - "static_web": Sitio web o SPA estático.
            - "batch": Procesamiento por lotes de gran volumen.

    Returns:
        Descripción de la arquitectura recomendada con los servicios AWS involucrados.
    """
    arquitecturas: dict[str, str] = {
        "api_rest": (
            "Arquitectura recomendada para API REST:\n"
            "  - Amazon API Gateway (enrutamiento y throttling)\n"
            "  - AWS Lambda (lógica de negocio serverless)\n"
            "  - Amazon DynamoDB (base de datos NoSQL de baja latencia)\n"
            "  - Amazon Cognito (autenticación y autorización)\n"
            "  - AWS WAF (protección contra ataques web)\n"
            "  Patrón: Serverless REST API con autenticación JWT."
        ),
        "streaming": (
            "Arquitectura recomendada para Streaming:\n"
            "  - Amazon Kinesis Data Streams (ingesta de eventos en tiempo real)\n"
            "  - AWS Lambda o Amazon Kinesis Data Analytics (procesamiento)\n"
            "  - Amazon S3 (almacenamiento de datos crudos / data lake)\n"
            "  - Amazon OpenSearch Service (búsqueda y visualización)\n"
            "  - Amazon CloudWatch (monitoreo de pipelines)\n"
            "  Patrón: Lambda Architecture con procesamiento en tiempo real."
        ),
        "ml_inference": (
            "Arquitectura recomendada para ML Inference:\n"
            "  - Amazon SageMaker Endpoints (despliegue de modelos)\n"
            "  - AWS Lambda (preprocesamiento y orquestación)\n"
            "  - Amazon API Gateway (exposición del endpoint de inferencia)\n"
            "  - Amazon S3 (almacenamiento de modelos y artefactos)\n"
            "  - Amazon CloudWatch + SageMaker Model Monitor (observabilidad)\n"
            "  Patrón: Serverless ML Inference con auto-scaling."
        ),
        "static_web": (
            "Arquitectura recomendada para Sitio Web Estático:\n"
            "  - Amazon S3 (alojamiento de archivos estáticos)\n"
            "  - Amazon CloudFront (CDN global con baja latencia)\n"
            "  - AWS Certificate Manager (certificado SSL/TLS gratuito)\n"
            "  - Amazon Route 53 (DNS y gestión de dominio)\n"
            "  - AWS CodePipeline (CI/CD para despliegues automáticos)\n"
            "  Patrón: JAMstack con distribución global via CDN."
        ),
        "batch": (
            "Arquitectura recomendada para Procesamiento Batch:\n"
            "  - AWS Batch (orquestación de jobs en contenedores)\n"
            "  - Amazon S3 (entrada y salida de datos)\n"
            "  - AWS Step Functions (coordinación de flujos de trabajo)\n"
            "  - Amazon ECR (registro de imágenes Docker)\n"
            "  - Amazon CloudWatch Events (programación de ejecuciones)\n"
            "  Patrón: Event-driven batch con contenedores administrados."
        ),
    }

    caso = caso_de_uso.lower().strip()
    if caso not in arquitecturas:
        opciones = ", ".join(arquitecturas.keys())
        return f"Caso de uso '{caso_de_uso}' no reconocido. Opciones válidas: {opciones}."

    return arquitecturas[caso]


@tool
def buscar_servicio_aws(categoria: str) -> str:
    """Lista los principales servicios AWS disponibles en una categoría.

    Devuelve un catálogo de servicios AWS agrupados por área tecnológica,
    con una breve descripción de cada servicio.

    Args:
        categoria: Categoría de servicios a consultar. Valores válidos:
            - "compute": Servicios de cómputo (VMs, contenedores, serverless).
            - "storage": Almacenamiento de objetos, bloques y archivos.
            - "database": Bases de datos relacionales, NoSQL y en memoria.
            - "ai": Inteligencia artificial y machine learning.
            - "networking": Redes, CDN, DNS y conectividad.

    Returns:
        Lista de servicios AWS de la categoría solicitada con sus descripciones.
    """
    catalogo: dict[str, dict[str, str]] = {
        "compute": {
            "Amazon EC2": "Máquinas virtuales escalables en la nube.",
            "AWS Lambda": "Cómputo serverless orientado a eventos.",
            "Amazon ECS": "Orquestación de contenedores Docker administrada.",
            "Amazon EKS": "Kubernetes administrado en AWS.",
            "AWS Fargate": "Cómputo serverless para contenedores (sin gestionar servidores).",
            "AWS Elastic Beanstalk": "Despliegue y escalado automático de aplicaciones web.",
        },
        "storage": {
            "Amazon S3": "Almacenamiento de objetos con durabilidad del 99.999999999%.",
            "Amazon EBS": "Volúmenes de almacenamiento en bloque para EC2.",
            "Amazon EFS": "Sistema de archivos NFS elástico y administrado.",
            "AWS Storage Gateway": "Integración híbrida entre on-premises y S3.",
            "Amazon Glacier": "Archivado de datos de bajo costo a largo plazo.",
        },
        "database": {
            "Amazon RDS": "Bases de datos relacionales administradas (MySQL, PostgreSQL, etc.).",
            "Amazon Aurora": "Base de datos relacional compatible con MySQL/PostgreSQL, alto rendimiento.",
            "Amazon DynamoDB": "Base de datos NoSQL clave-valor con latencia de milisegundos.",
            "Amazon ElastiCache": "Caché en memoria con Redis o Memcached.",
            "Amazon Redshift": "Data warehouse columnar para análisis a escala de petabytes.",
            "Amazon DocumentDB": "Base de datos de documentos compatible con MongoDB.",
        },
        "ai": {
            "Amazon Bedrock": "Acceso a modelos fundacionales de IA generativa vía API.",
            "Amazon SageMaker": "Plataforma completa para entrenar y desplegar modelos ML.",
            "Amazon Rekognition": "Análisis de imágenes y video con visión por computadora.",
            "Amazon Comprehend": "Procesamiento de lenguaje natural (NLP) administrado.",
            "Amazon Polly": "Conversión de texto a voz realista.",
            "Amazon Transcribe": "Transcripción automática de audio a texto.",
            "Amazon Lex": "Creación de chatbots con IA conversacional.",
        },
        "networking": {
            "Amazon VPC": "Red privada virtual aislada dentro de AWS.",
            "Amazon CloudFront": "CDN global con más de 400 puntos de presencia.",
            "Amazon Route 53": "DNS escalable y registro de dominios.",
            "AWS Direct Connect": "Conexión dedicada entre on-premises y AWS.",
            "AWS Transit Gateway": "Hub central para conectar múltiples VPCs y redes.",
            "Elastic Load Balancing": "Distribución de tráfico entre instancias (ALB, NLB, CLB).",
        },
    }

    cat = categoria.lower().strip()
    if cat not in catalogo:
        opciones = ", ".join(catalogo.keys())
        return f"Categoría '{categoria}' no reconocida. Opciones válidas: {opciones}."

    servicios = catalogo[cat]
    lineas = [f"Servicios AWS — categoría '{cat}':"]
    for nombre, descripcion in servicios.items():
        lineas.append(f"  - {nombre}: {descripcion}")
    return "\n".join(lineas)
