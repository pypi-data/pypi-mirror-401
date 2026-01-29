"""
Usage examples for Prompt XMLifier.

Demonstrates various ways to convert prompts to XML-tagged format
following Anthropic's official best practices.

Run this file directly to see examples in action:
    python -m prompt_xmlifier.examples
"""

from .xmlifier import PromptXMLifier, ParserConfig


def example_basic_conversion():
    """Basic prompt conversion example."""
    print("=" * 60)
    print("Example 1: Basic Prompt Conversion")
    print("=" * 60)

    prompt = """
    Please analyze the following Python code and identify any bugs or improvements.
    Focus on performance and security issues.

    def get_user(id):
        query = "SELECT * FROM users WHERE id = " + id
        return db.execute(query)

    The output should be a list of issues with severity ratings.
    """

    xmlifier = PromptXMLifier()
    result = xmlifier.convert(prompt)

    print("\nOriginal Prompt:")
    print("-" * 40)
    print(prompt)

    print("\nXMLified Prompt:")
    print("-" * 40)
    print(result.to_xml())
    print()


def example_labeled_sections():
    """Example with explicitly labeled sections."""
    print("=" * 60)
    print("Example 2: Explicitly Labeled Sections")
    print("=" * 60)

    prompt = """
Task:
Create a REST API endpoint for user authentication

Context:
We are building a microservices architecture using FastAPI.
The authentication should use JWT tokens.

Instructions:
1. Create a POST endpoint at /auth/login
2. Validate email and password
3. Return a JWT token on success
4. Handle errors gracefully

Constraints:
- Token expiry: 24 hours
- Use bcrypt for password hashing
- Follow OWASP security guidelines

Output:
Provide the complete Python code with type hints and docstrings.
    """

    xmlifier = PromptXMLifier()
    result = xmlifier.convert(prompt)

    print("\nOriginal Prompt:")
    print("-" * 40)
    print(prompt)

    print("\nXMLified Prompt:")
    print("-" * 40)
    print(result.to_xml())
    print()


def example_with_xml_tags():
    """Example where input already has some XML tags."""
    print("=" * 60)
    print("Example 3: Input with Existing XML Tags")
    print("=" * 60)

    prompt = """
<role>
You are a senior database architect specializing in Snowflake.
</role>

<task>
Design a medallion architecture for our data lakehouse.
</task>

<context>
We have multiple data sources including:
- CRM system (Salesforce)
- ERP system (SAP)
- IoT sensors (real-time data)
</context>

<constraints>
- Must support both batch and streaming
- Data retention: 7 years
- GDPR compliant
</constraints>
    """

    xmlifier = PromptXMLifier()
    result = xmlifier.convert(prompt)

    print("\nOriginal Prompt:")
    print("-" * 40)
    print(prompt)

    print("\nXMLified Prompt (preserved tags):")
    print("-" * 40)
    print(result.to_xml())
    print()


def example_json_output():
    """Example showing JSON output format."""
    print("=" * 60)
    print("Example 4: JSON Output Format")
    print("=" * 60)

    import json

    prompt = """
    Help me write a function that calculates the Fibonacci sequence.
    The function should be efficient and handle large numbers.
    Include examples of usage.
    """

    xmlifier = PromptXMLifier()
    result = xmlifier.convert(prompt)

    print("\nOriginal Prompt:")
    print("-" * 40)
    print(prompt)

    print("\nJSON Output:")
    print("-" * 40)
    print(json.dumps(result.to_dict(), indent=2))
    print()


def example_custom_config():
    """Example with custom parser configuration."""
    print("=" * 60)
    print("Example 5: Custom Parser Configuration")
    print("=" * 60)

    prompt = """
    You are an expert code reviewer.

    Review this code for security vulnerabilities.

    Be thorough but concise in your analysis.
    """

    # Custom configuration with higher confidence threshold
    config = ParserConfig(
        min_section_length=5,
        confidence_threshold=0.5,
        nest_related_tags=False
    )

    xmlifier = PromptXMLifier(config)
    result = xmlifier.convert(prompt)

    print("\nOriginal Prompt:")
    print("-" * 40)
    print(prompt)

    print("\nXMLified Prompt (high confidence):")
    print("-" * 40)
    print(result.to_xml())

    # Show confidence scores
    print("\nSection Confidence Scores:")
    print("-" * 40)
    for section in result.sections:
        tag_name = section.tag.name if section.tag else "untagged"
        print(f"  <{tag_name}>: {section.confidence:.2f}")
    print()


def example_bilingual():
    """Example with Spanish prompt (bilingual support)."""
    print("=" * 60)
    print("Example 6: Spanish Prompt (Bilingual Support)")
    print("=" * 60)

    prompt = """
Tarea:
Crear un sistema de autenticacion para una aplicacion web.

Contexto:
Estamos desarrollando una plataforma educativa para DuocUC.
Los usuarios incluyen estudiantes, profesores y administradores.

Instrucciones:
1. Implementar login con email y contrasena
2. Agregar autenticacion de dos factores
3. Manejar roles y permisos

Restricciones:
- Cumplir con normativas de proteccion de datos
- Usar encriptacion AES-256
- Tiempo de sesion maximo: 8 horas

Ejemplo:
Usuario: estudiante@duoc.cl
Rol: STUDENT
Permisos: VIEW_COURSES, SUBMIT_ASSIGNMENTS
    """

    xmlifier = PromptXMLifier()
    result = xmlifier.convert(prompt)

    print("\nPrompt Original:")
    print("-" * 40)
    print(prompt)

    print("\nPrompt XMLificado:")
    print("-" * 40)
    print(result.to_xml())
    print()


def example_complex_prompt():
    """Example with a complex, multi-part prompt."""
    print("=" * 60)
    print("Example 7: Complex Multi-Part Prompt")
    print("=" * 60)

    prompt = """
Role: You are a senior Snowflake data engineer at a Fortune 500 company.

Task: Design and implement a real-time data pipeline.

Context:
Our company processes 10TB of data daily from multiple sources.
Current pain points:
- High latency in data freshness
- Manual ETL processes
- No data quality checks

Do:
- Use Snowflake native features (Streams, Tasks, Dynamic Tables)
- Implement incremental loading patterns
- Add comprehensive error handling
- Include observability (logging, metrics)

Do Not:
- Use external orchestration tools
- Create unnecessary data copies
- Hardcode credentials
- Skip data validation

Input Data:
Source: S3 bucket s3://company-data/raw/
Format: JSON and Parquet files
Volume: ~500GB per hour
Schema: See attached data dictionary

Output:
1. Architecture diagram (mermaid format)
2. SQL scripts for all objects
3. Deployment guide
4. Monitoring dashboard config

Thinking:
Walk through your design decisions step by step, explaining the tradeoffs.
    """

    xmlifier = PromptXMLifier()
    result = xmlifier.convert(prompt)

    print("\nOriginal Prompt:")
    print("-" * 40)
    print(prompt)

    print("\nXMLified Prompt:")
    print("-" * 40)
    print(result.to_xml(include_wrapper=True))
    print()


def run_all_examples():
    """Run all examples."""
    example_basic_conversion()
    example_labeled_sections()
    example_with_xml_tags()
    example_json_output()
    example_custom_config()
    example_bilingual()
    example_complex_prompt()

    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
    print()
    print("For more information, see:")
    print("  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags")
    print()


if __name__ == "__main__":
    run_all_examples()
