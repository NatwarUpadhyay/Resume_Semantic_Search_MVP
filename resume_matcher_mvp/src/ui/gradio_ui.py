import gradio as gr

from ..services.mapping_service import MappingService


class GradioUI:
    """
    Handles the Gradio user interface for the Profile-to-Role Mapper.
    """

    def __init__(self, mapping_service: MappingService):
        """
        Initializes the UI with a mapping service.

        Args:
            mapping_service: An instance of MappingService.
        """
        self.mapping_service = mapping_service

    def _map_profile_wrapper(self, student_data: str, jd: str) -> tuple[str, str, str, str]:
        """
        A wrapper for the mapping service to format the output for Gradio.
        """
        category, role, confidence, keywords = self.mapping_service.map_profile(student_data, jd)

        confidence_str = f"{confidence:.1%}"
        keywords_str = ", ".join(keywords)

        return category, role, confidence_str, keywords_str

    def create_interface(self):
        """
        Creates and configures the Gradio interface.
        """
        with gr.Blocks(title="Profile-to-Role Mapper", theme=gr.themes.Soft()) as interface:
            gr.Markdown("# 🧑‍🎓 Profile-to-Role Mapper")
            gr.Markdown("Enter student data and a job description to find the best-fit profile category and role.")

            with gr.Row():
                with gr.Column(scale=1):
                    student_data_input = gr.Textbox(
                        label="Student Data",
                        placeholder="Paste the student's profile data here...",
                        lines=20,
                        max_lines=40,
                    )
                with gr.Column(scale=1):
                    jd_input = gr.Textbox(
                        label="Job Description",
                        placeholder="Paste the job description here...",
                        lines=20,
                        max_lines=40,
                    )

            map_button = gr.Button("🗺️ Map Profile", variant="primary")

            gr.Markdown("## 💡 Mapping Results")
            with gr.Row():
                category_output = gr.Textbox(label="Profile Category", interactive=False)
                role_output = gr.Textbox(label="Predicted Role", interactive=False)

            with gr.Row():
                confidence_output = gr.Textbox(label="Confidence Score", interactive=False)
                keywords_output = gr.Textbox(label="Matched Keywords", interactive=False)

            # Event handler for the button click
            map_button.click(
                fn=self._map_profile_wrapper,
                inputs=[student_data_input, jd_input],
                outputs=[category_output, role_output, confidence_output, keywords_output],
            )

            # Add some examples
            gr.Examples(
                examples=[
                    [
                        """**Education**
                        postgraduate - Bharathidasan Institute of Management, Trichy - 7.92 - cgpa
                        **Projects**
                        Projects - sales prediction model - Developed a sales prediction model for Prompt Company using R and machine learning algorithms like XGBoost.
                        """,
                        """We are looking for a Data Analyst to join our team. The ideal candidate will have experience with SQL, Python, and data visualization tools like Tableau. Responsibilities include building dashboards and generating reports.""",
                    ],
                    [
                        """**Work experience and internships**
                        internship - Marmore MENA Intelligence Pvt Ltd - 2024-04-01 - 2024-05-01 - Conducted competitor analysis on websites and social media, developing a strategic enhancement plan.
                        """,
                        """Seeking a Strategy Consultant to help our clients with market entry strategies. Must have strong analytical and research skills. MBA preferred.""",
                    ]
                ],
                inputs=[student_data_input, jd_input],
            )

        return interface
