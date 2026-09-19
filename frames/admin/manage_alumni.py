# ==========================================
# DLSAU Alumni Tracking System
# frames/admin/manage_alumni.py
# ==========================================

import tkinter as tk
from tkinter import ttk

from frames.base_page import BasePage
from models.user_model import UserModel
from utils.session import set_selected_alumni
from utils.export_excel import export_alumni
from components.button import PrimaryButton, SecondaryButton
from widgets.confirm_dialog import ConfirmDialog

from utils.email_sender import send_email

class ManageAlumniPage(BasePage):

    def __init__(self, parent, controller):

        super().__init__(parent, controller)

        self.controller = controller
        self.user_model = UserModel()

        content = self.create_content_pane()

        # ==========================
        # TITLE
        # ==========================

        self.create_title(
            "Manage Alumni", content
        ).pack(pady=20)

        self.total_label = tk.Label(
            content,
            text="Total Alumni: 0",
            bg=self.BG_COLOR,
            font=("Helvetica", 14, "bold")
        )

        self.total_label.pack(pady=(0, 10))

        # ==========================
        # SEARCH
        # ==========================

        search_frame = tk.Frame(
            content,
            bg=self.BG_COLOR
        )

        search_frame.pack(pady=10)

        tk.Label(
            search_frame,
            text="Search:",
            bg=self.BG_COLOR
        ).pack(side="left")

        self.search_entry = tk.Entry(
            search_frame,
            width=30
        )

        self.search_entry.pack(
            side="left",
            padx=10
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search()
        )

        PrimaryButton(
            search_frame,
            "Search",
            self.search
        ).pack(side="left")

        # ==========================
        # TABLE
        # ==========================

        columns = (
            "student",
            "name",
            "course",
            "year",
            "status"
        )

        table_frame = tk.Frame(
            content,
            bg=self.BG_COLOR
        )

        # NOTE: table_frame is packed further below, *after* the button
        # rows. Packing the buttons first with side="bottom" reserves
        # their space regardless of window size, so they can never get
        # squeezed off-screen — only the table area shrinks/scrolls.

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
            yscrollcommand=scrollbar.set
        )

        style = ttk.Style()

        style.configure(
            "Treeview",
            font=("Helvetica", 14),
            rowheight=30
        )

        style.configure(
            "Treeview.Heading",
            font=("Helvetica", 14, "bold")
        )

        self.tree.heading(
            "student",
            text="Student No."
        )

        self.tree.heading(
            "name",
            text="Name"
        )

        self.tree.heading(
            "course",
            text="Course"
        )

        self.tree.heading(
            "year",
            text="Graduation"
        )

        self.tree.heading(
            "status",
            text="Status"
        )

        self.tree.column(
            "student",
            width=140,
            anchor="center"
        )

        self.tree.column(
            "name",
            width=260
        )

        self.tree.column(
            "course",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "year",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "status",
            width=120,
            anchor="center"
        )

        scrollbar.config(
            command=self.tree.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==========================
        # BUTTONS
        # ==========================
        # Packed with side="bottom" so they always keep their space,
        # regardless of window size. back_row is packed first so it
        # anchors to the very bottom edge; button_frame stacks above it.

        back_row = tk.Frame(
            content,
            bg=self.BG_COLOR
        )

        back_row.pack(side="bottom", pady=(0, 16))

        SecondaryButton(
            back_row,
            text="\u2190 Back to Dashboard",
            command=lambda:
            controller.show_frame(
                "AdminDashboardPage"
            ),
            width=22,
        ).pack()

        button_frame = tk.Frame(
            content,
            bg=self.BG_COLOR
        )

        button_frame.pack(side="bottom", pady=(8, 8))

        PrimaryButton(
            button_frame,
            "Approve",
            self.approve
        ).pack(side="left", padx=5, pady=4)

        PrimaryButton(
            button_frame,
            "Reject",
            self.reject
        ).pack(side="left", padx=5, pady=4)

        PrimaryButton(
            button_frame,
            "Delete",
            self.delete
        ).pack(side="left", padx=5, pady=4)

        PrimaryButton(
            button_frame,
            "View Details",
            self.view_details
        ).pack(side="left", padx=5, pady=4)

        PrimaryButton(
            button_frame,
            "Export",
            self.export_excel
        ).pack(side="left", padx=5, pady=4)

        # ==========================
        # TABLE
        # ==========================
        # Packed last so it fills whatever vertical space remains
        # between the search bar above and the button rows below.

        table_frame.pack(
            pady=10,
            fill="both",
            expand=True
        )

        self.load_users()

    # ==========================================

    def load_users(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        users = self.user_model.get_all_alumni()

        self.total_label.config(
            text=f"Total Alumni: {len(users)}"
        )

        for user in users:

            fullname = (
                f"{user['last_name']}, "
                f"{user['first_name']}"
            )

            self.tree.insert(
                "",
                "end",
                iid=user["id"],
                values=(
                    user["student_number"] or "N/A",
                    fullname,
                    user["course"],
                    user["graduation_year"],
                    user["status"]
                )
            )

    # ==========================================

    def get_selected(self):

        selected = self.tree.focus()

        if not selected:

            self.toast_warning("Please select an alumni.")

            return None

        return int(selected)

    # ==========================================

    def approve(self):

        user_id = self.get_selected()

        if user_id is None:
            return

        self.user_model.update_status(
            user_id,
            "Approved"
        )

        user = self.user_model.get_user_by_id(
            user_id
        )

        subject = (
            "DLSAU Alumni Tracking System - Account Approved"
        )

        body = f"""
    Dear {user['first_name']} {user['last_name']},

    Congratulations!

    Your registration for the DLSAU Alumni Tracking System has been approved by the administrator.

    You may now log in using the following account:

    Username: {user['username']}

    Please use the password you created during registration.

    Thank you for being part of the DLSAU alumni community.

    Regards,

    Group 2 Development Team
    De La Salle Araneta University: Alumni Tracking System
    """

        success = send_email(
            user["email"],
            subject,
            body
        )

        if success:

            self.toast_success("Account status updated. Email notification sent successfully.")

        else:

            self.toast_warning(
                "Account status was updated, but the email notification could not be sent.",
                "Email Error"
            )

        self.load_users()

    # ==========================================

    def reject(self):

        user_id = self.get_selected()

        if user_id is None:
            return

        self.user_model.update_status(
            user_id,
            "Rejected"
        )

        user = self.user_model.get_user_by_id(
            user_id
        )

        subject = (
            "DLSAU Alumni Tracking System - Registration Update"
        )

        body = f"""
    Dear {user['first_name']} {user['last_name']},

    Thank you for registering for the DLSAU Alumni Tracking System.

    After reviewing your registration, we regret to inform you that your account has not been approved.

    If you believe this was made in error or if you need further clarification, please contact the system administrator.

    Thank you for your understanding.

    Regards,

    Group 2 Development Team
    De La Salle Araneta University: Alumni Tracking System
    """

        success = send_email(
            user["email"],
            subject,
            body
        )

        if success:

            self.toast_success("Account status updated. Email notification sent successfully.")

        else:

            self.toast_warning(
                "Account status was updated, but the email notification could not be sent.",
                "Email Error"
            )

        self.load_users()

    # ==========================================

    def delete(self):

        user_id = self.get_selected()

        if user_id is None:
            return

        user = self.user_model.get_user_by_id(user_id)

        name = (
            f"{user['first_name']} {user['last_name']}"
            if user else "this alumni"
        )

        confirmed = ConfirmDialog.ask(
            self,
            title="Delete Alumni Record",
            message=f"Are you sure you want to delete {name}?",
            detail="This will permanently remove their record. This action cannot be undone.",
            confirm_text="Delete",
            cancel_text="Cancel",
            danger=True,
        )

        if not confirmed:
            return

        self.user_model.delete_user(user_id)
        self.load_users()
        self.toast_success("Alumni deleted successfully.")

    # ==========================================

    def view_details(self):

        user_id = self.get_selected()

        if user_id is None:
            return

        user = self.user_model.get_user_by_id(
            user_id
        )

        set_selected_alumni(user)

        details_page = self.controller.frames[
            "AlumniDetailsPage"
        ]

        details_page.load_profile()

        self.controller.show_frame(
            "AlumniDetailsPage"
        )

    # ==========================================

    def search(self):

        keyword = self.search_entry.get().strip()

        if keyword == "":
            self.load_users()
            return

        users = self.user_model.search_users(
            keyword
        )

        for row in self.tree.get_children():
            self.tree.delete(row)

        for user in users:

            fullname = (
                f"{user['last_name']}, "
                f"{user['first_name']}"
            )

            self.tree.insert(
                "",
                "end",
                iid=user["id"],
                values=(
                    user["student_number"] or "N/A",
                    fullname,
                    user["course"],
                    user["graduation_year"],
                    user["status"]
                )
            )

    # ==========================================

    def export_excel(self):

        success = export_alumni()

        if success:

            self.toast_success("Alumni report exported successfully.")