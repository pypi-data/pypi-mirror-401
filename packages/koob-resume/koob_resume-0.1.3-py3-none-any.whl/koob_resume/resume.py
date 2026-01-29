"""resume.py: Create a PDF resume."""

from fpdf import FPDF

# Color constants
COLOR_BLACK = (0, 0, 0)
COLOR_TEXT = (50, 50, 50)
COLOR_LINK = (30, 80, 160)
COLOR_SEPARATOR = (150, 150, 150)
COLOR_LINE = (30, 71, 95)


class Resume:
    """A class responsible for managing and rendering a Resume."""

    def __init__(self, data):
        """
        Initialize the Resume with the raw data dictionary.

        Args:
        ----
            data (dict): The dictionary loaded from the JSON file.

        """
        self.data = data

    def render(self, output_path="resume.pdf"):
        """Orchestrate the rendering of the resume."""
        pdf = FPDF(format="A4")
        pdf.MARKDOWN_LINK_UNDERLINE = False
        pdf.add_page()

        self.render_header(pdf)
        self.render_summary(pdf)
        self.render_skills(pdf)
        self.render_experience(pdf)
        self.render_education(pdf)

        pdf.output(output_path)
        print(f"Resume saved to: {output_path}")

    def render_section_header(self, pdf, title):
        """Render a section header with underline."""
        font_size = self.data.get("font_sizes", {}).get("section_header", 14)
        pdf.set_y(pdf.get_y() + 3)
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "", font_size)
        pdf.set_text_color(*COLOR_BLACK)
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align="L")
        pdf.set_draw_color(*COLOR_LINE)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.ln(2)

    def render_bullet_item(self, pdf, text, bullet_width=3):
        """Render a bullet point item with ZapfDingbats bullet."""
        body_size = self.data.get("font_sizes", {}).get("body", 12)
        start_x = pdf.get_x()

        pdf.set_x(start_x)
        pdf.set_font("ZapfDingbats", "", 5)
        pdf.write(5, "l")  # 'l' in ZapfDingbats = bullet
        pdf.set_font("Helvetica", "", body_size)

        pdf.set_left_margin(start_x + bullet_width)
        pdf.set_x(start_x + bullet_width)

        pdf.multi_cell(0, 5, text, markdown=True)

        pdf.set_left_margin(start_x)
        pdf.ln(2)

    def render_header(self, pdf):
        """Render the header section of the resume."""
        if pdf.page_no() == 1:
            name_size = self.data.get("font_sizes", {}).get("name", 25)
            role_size = self.data.get("font_sizes", {}).get("role", 17)
            body_size = self.data.get("font_sizes", {}).get("body", 12)
            y_start = pdf.get_y()
            pdf.set_font("Helvetica", "", name_size)
            pdf.set_text_color(*COLOR_BLACK)
            pdf.cell(
                0,
                10,
                f"**{self.data['p_info']['name'].upper()}**",
                new_x="LMARGIN",
                new_y="NEXT",
                align="L",
                markdown=True,
            )
            pdf.set_font("Helvetica", "", role_size)
            pdf.set_text_color(*COLOR_BLACK)
            pdf.cell(
                0,
                7,
                self.data["job_target"]["role"],
                new_x="LMARGIN",
                new_y="NEXT",
                align="L",
            )
            y_line = pdf.get_y()
            pdf.set_y(y_start)
            pdf.set_font("Helvetica", "", body_size)
            pdf.set_text_color(*COLOR_TEXT)
            pdf.cell(
                0,
                6,
                self.data["p_info"]["phone"],
                new_x="LMARGIN",
                new_y="NEXT",
                align="R",
            )
            pdf.set_text_color(*COLOR_LINK)
            pdf.cell(
                0,
                6,
                f"[{self.data['p_info']['email']}](mailto:{self.data['p_info']['email']})",
                # 0, 6, self.data['p_info']['email'],
                new_x="LMARGIN",
                new_y="NEXT",
                align="R",
                markdown=True,
            )
            pdf.cell(
                0,
                6,
                f"[{self.data['p_info']['linkedin']}](https://{self.data['p_info']['linkedin']})",
                new_x="RIGHT",
                new_y="TOP",
                align="R",
                markdown=True,
            )
            pdf.set_y(y_line + 1)
            pdf.set_draw_color(*COLOR_LINE)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
            pdf.ln(3)

    def render_summary(self, pdf):
        """Render the summary section of the resume."""
        body_size = self.data.get("font_sizes", {}).get("body", 12)
        summary = self.data.get("summary", "")
        pdf.set_font("Helvetica", "", body_size)
        pdf.set_text_color(*COLOR_TEXT)
        pdf.multi_cell(0, 6, summary, markdown=True)

    def render_skills(self, pdf):
        """Render the skills section of the resume."""
        body_size = self.data.get("font_sizes", {}).get("body", 12)
        skills_dict = self.data.get("skills", {})
        title = self.data.get("section_titles", {}).get("skills", "Skills")
        self.render_section_header(pdf, title)
        pdf.set_font("Helvetica", "", body_size)
        for category, items in skills_dict.items():
            pdf.set_text_color(*COLOR_BLACK)
            pdf.set_font("Helvetica", "B", body_size)
            clean_category = category.replace("_", " ")
            pdf.write(7, f"{clean_category}: ")
            pdf.set_text_color(*COLOR_TEXT)
            pdf.set_font("Helvetica", "", body_size)
            items_str = ", ".join(items)
            pdf.write(7, items_str)
            pdf.ln(7)

    def render_experience(self, pdf):
        """Render the experience section of the resume."""
        body_size = self.data.get("font_sizes", {}).get("body", 12)
        experience_dict = self.data.get("experience", {})
        title = self.data.get("section_titles", {}).get("experience", "Experience")
        self.render_section_header(pdf, title)
        pdf.set_font("Helvetica", "", body_size)
        pdf.set_text_color(*COLOR_TEXT)
        for entry in experience_dict:
            pdf.set_font("Helvetica", "", body_size)
            pdf.set_text_color(*COLOR_BLACK)
            pdf.cell(
                0,
                6,
                "**" + entry["title"],
                new_x="RIGHT",
                new_y="TOP",
                align="L",
                markdown=True,
            )
            pdf.set_text_color(*COLOR_TEXT)
            pdf.cell(0, 6, entry["duration"], new_x="LMARGIN", new_y="NEXT", align="R")
            pdf.cell(
                pdf.get_string_width(entry["company"]),
                6,
                entry["company"],
                new_x="RIGHT",
                new_y="TOP",
                align="L",
                markdown=True,
            )
            pdf.set_text_color(*COLOR_SEPARATOR)
            pdf.cell(
                pdf.get_string_width(" | "),
                6,
                " | ",
                new_x="RIGHT",
                new_y="TOP",
                align="L",
                markdown=True,
            )
            pdf.set_text_color(*COLOR_LINK)
            pdf.cell(
                0,
                6,
                f"[{entry['website']}](https://{entry['website']})",
                new_x="LMARGIN",
                new_y="NEXT",
                align="L",
                markdown=True,
            )
            pdf.set_text_color(*COLOR_TEXT)
            pdf.set_font("Helvetica", "", body_size)
            pdf.multi_cell(0, 6, entry["summary"], markdown=True)
            pdf.ln(2)

            responsibilities = entry.get("responsibilities", [])
            if isinstance(responsibilities, list):
                for resp in responsibilities:
                    self.render_bullet_item(pdf, resp)

    def render_education(self, pdf):
        """Render the education section with certifications first (reverse chron)."""
        body_size = self.data.get("font_sizes", {}).get("body", 12)
        title = self.data.get("section_titles", {}).get(
            "education", "Education & Certifications"
        )
        self.render_section_header(pdf, title)

        # Certifications first (more recent) - only if present
        certifications = self.data.get("certifications", [])
        if certifications:
            cert_title = self.data.get("section_titles", {}).get(
                "certifications", "Recent Industry Certifications"
            )
            pdf.set_font("Helvetica", "", body_size)
            pdf.set_text_color(*COLOR_BLACK)
            pdf.cell(
                0,
                6,
                f"**{cert_title}",
                new_x="RIGHT",
                new_y="TOP",
                align="L",
                markdown=True,
            )
            pdf.set_text_color(*COLOR_TEXT)
            pdf.ln(6)

            for cert in certifications:
                pdf.set_font("Helvetica", "", body_size)
                pdf.cell(
                    0,
                    6,
                    f"- {cert.get('cert', '')}",
                    new_x="RIGHT",
                    new_y="TOP",
                    align="L",
                )
                pdf.cell(
                    0,
                    6,
                    f"{cert.get('year', '')}",
                    new_x="LMARGIN",
                    new_y="NEXT",
                    align="R",
                )
            pdf.ln(3)

        # Education after (older)
        for entry in self.data.get("education", []):
            pdf.set_font("Helvetica", "", body_size)
            pdf.set_text_color(*COLOR_BLACK)
            pdf.cell(
                0,
                6,
                "**" + entry["degree"],
                new_x="RIGHT",
                new_y="TOP",
                align="L",
                markdown=True,
            )
            pdf.set_text_color(*COLOR_TEXT)
            pdf.cell(0, 6, entry["duration"], new_x="LMARGIN", new_y="NEXT", align="R")
            pdf.cell(
                0,
                6,
                entry["institution"],
                new_x="LMARGIN",
                new_y="NEXT",
                align="L",
                markdown=True,
            )
            pdf.multi_cell(0, 6, entry["summary"], markdown=True)
            pdf.ln(2)
