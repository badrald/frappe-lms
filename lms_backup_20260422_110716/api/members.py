import frappe 
import uuid


@frappe.whitelist()
def get_all_members():
    members = frappe.get_all("Member", fields=["*"])
    
    for member in members:
        if member.user:
            try:
                user = frappe.get_doc("User", member.user)
                member.user_name = user.full_name
                member.user_email = user.email
                member.user_image = user.user_image
            except Exception:
                member.user_name = ""
                member.user_email = ""
                member.user_image = ""
        else:
            member.user_name = ""
            member.user_email = ""
            member.user_image = ""
        
    return members


@frappe.whitelist()
def get_member_by_id(member_id):
    member = frappe.get_doc("Member", member_id)
    return member


def create_user(user_data):
    """
    Create a User with the Member role.
    
    Args:
        first_name (str): User's first name
        last_name (str): User's last name
        email (str): User's email address
        phone_number (str): User's phone number
        user_image (str, optional): URL or path to user's image
        
    Returns:
        User: Created user document
    """
    user = frappe.new_doc("User")
    user.email = user_data.get('email')
    user.first_name = user_data.get('first_name')
    user.last_name = user_data.get('last_name')
    user.phone = user_data.get('phone_number')
    user.user_image = user_data.get('user_image')
    user.address = user_data.get('address')
    user.role = "Member"
    password = uuid.uuid4().hex[:8]
    user.reset_password(password)
    frappe.sendmail([user.email], "Welcome to the Library Management System", "Your password is: " + password , "Please Change your password after login")
    user.send_welcome_email = 0
    user.add_roles("Member")
    user.save()

    return user


@frappe.whitelist()
def create_user_for_member(**data):
    """
    Create a User for the member with the Member role, complete member data, and link the user to the member.
    
    Args:
        data: A data object containing member information like email, first_name, etc.
        
    Returns:
        dict: A dictionary containing the created user and member information.
    """
    # Create a new User document
    user = create_user(data) 

    
    # Update the member document with complete information
    member_doc = frappe.get_doc("Member", data.get('member_id'))
    member_doc.user = user.name
    member_doc.memeber_name = user.full_name
    member_doc.phone_number = user.phone
    member_doc.address = user.address
    member_doc.join_date = data.get('join_date')
    member_doc.member_type = data.get('member_type')
    member_doc.is_membership_valid = data.get('is_membership_valid')
    member_doc.save()
    
    return {
        "user": user,
        "member": member_doc
    }