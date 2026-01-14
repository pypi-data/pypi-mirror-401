from pygeai.organization.managers import OrganizationManager

manager = OrganizationManager()

response = manager.add_project_member(
    project_id="1956c032-3c66-4435-acb8-6a06e52f819f",
    user_email="newuser@example.com",
    roles=["Project member", "Project administrator"]
)
print(f"response: {response}")
