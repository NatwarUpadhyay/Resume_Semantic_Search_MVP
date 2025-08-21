from src.core.text_profile_parser import TextProfileParser
from src.core.domain_classifier import DomainClassifier
from src.services.mapping_service import MappingService
from src.ui.gradio_ui import GradioUI


def main():
    """
    Main function to initialize and launch the application.
    """
    # 1. Initialize core components
    text_parser = TextProfileParser()
    domain_classifier = DomainClassifier()

    # 2. Initialize the mapping service
    mapping_service = MappingService(parser=text_parser, classifier=domain_classifier)

    # 3. Initialize the Gradio UI
    gradio_ui = GradioUI(mapping_service=mapping_service)

    # 4. Create and launch the interface
    interface = gradio_ui.create_interface()
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
    )


if __name__ == "__main__":
    main()
