from flask import Flask, render_template, request, redirect, url_for, session, abort, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from functools import wraps

from OrmMetadata.Classes import *
from OrmMetadata.User import *

from datetime import datetime
import service
import logging

log_level = logging.DEBUG

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config["DEBUG"] = log_level == logging.DEBUG
app.secret_key = 'njasndbmnawgekj'
app.config['SESSION_PERMANENT'] = False
login_manager = LoginManager(app)
login_manager.login_view = 'login'
logging.basicConfig(level=log_level)


@login_manager.user_loader
def load_user(user_id):
    return dbsession.get(User, int(user_id))


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = service.checkLoginUser(username, password)
        if user:
            login_user(user)
            if user.role.name == 'admin':
                return redirect(url_for("admin"))
            if user.role.name == 'warehouseworker':
                return redirect(url_for('select_warehouse'))
            if user.role.name == 'helper':
                return redirect(url_for('select_location'))
        
        error = 'Wrong credentials, login failed!'
        return render_template('login.html', error=error)
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')



@app.route("/select_warehouse", methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('select_warehouse')
def select_warehouse():
    if request.method == 'POST':
        warehouse_id = request.form['selected_warehouse']
        return redirect(url_for('warehouse_deliveries', warehouse_id=warehouse_id))

    warehouses = service.getWarehouses()
    return render_template('select_warehouse.html', warehouses=warehouses)

@app.route("/<int:warehouse_id>/deliveries")
@login_required
@service.userRolesRequired('<int>/deliveries')
def warehouse_deliveries(warehouse_id):
    deliveries = service.getDeliveriesByDepature(warehouse_id)
    all_statuses = service.getAllStatuses()

    for delivery in deliveries:
        delivery.boxes_count = service.getBoxCountByDelivery(delivery.id)

    return render_template('deliveries.html', deliveries=deliveries, warehouse_id=warehouse_id, all_statuses=all_statuses)

@app.route("/<int:warehouse_id>/create_delivery", methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('<int/create_delivery')
def create_delivery(warehouse_id):
    if request.method == 'POST':
        project_id = request.form['project_id']
        destination_name = request.form['destination_name']
        status_name = request.form['status_name']
        arrival_date_tmp = request.form['arrival_date']


        arrival_date = datetime.strptime(arrival_date_tmp, '%Y-%m-%d').date()

        service.createDelivery(warehouse_id, status_name, arrival_date, project_id)
        return redirect(url_for('warehouse_deliveries', warehouse_id=warehouse_id))

    all_locations = service.getAllLocations()
    all_statuses = service.getAllStatuses()
    all_projects = service.getAllProjects()
    return render_template('create_delivery.html', locations=all_locations, statuses=all_statuses, warehouse_id=warehouse_id, projects=all_projects)

@app.route("/<int:warehouse_id>/create_delivery/create_project", methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('<int/create_delivery/create_project')
def create_project(warehouse_id):
    if request.method == 'POST':
        project_name = request.form['project_name']
        destination_name = request.form['destination_name']

        service.createProject(project_name, destination_name)
        return redirect(url_for('create_delivery', warehouse_id=warehouse_id))

    locations = service.getDestinations()

    return render_template('create_project.html', warehouse_id=warehouse_id)

@app.route("/<int:warehouse_id>/deliveries/<int:delivery_id>/boxes")
@login_required
@service.userRolesRequired('<int>/deliveries/<int>/boxes')
def warehouse_boxes(warehouse_id, delivery_id):
    boxes = service.getBoxesByDelivery(delivery_id)
    all_statuses = service.getAllStatuses()
    return render_template('boxes.html', boxes=boxes, warehouse_id=warehouse_id, delivery_id=delivery_id, all_statuses=all_statuses)

@app.route("/<int:warehouse_id>/deliveries/<int:delivery_id>/create_box", methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('<int>/deliveries/<int>/create_box')
def create_box(warehouse_id, delivery_id):
    if request.method == 'POST':
        category_name = request.form['category_name']
        status_name = request.form['status_name']
        box_description = request.form['box_description']
        resource_ids = request.form.getlist('resource_ids')

        box_id = service.createBox(category_name, status_name, box_description, delivery_id)
        service.updateBoxIdRessource(box_id, resource_ids)

        return redirect(url_for('warehouse_boxes', warehouse_id=warehouse_id, delivery_id=delivery_id))

    all_categories = service.getAllCategories()
    all_statuses = service.getAllStatuses()
    all_ressources_without_box = service.getRessourcesWithoutBox()

    return render_template('create_box.html', warehouse_id=warehouse_id, delivery_id=delivery_id, all_categories=all_categories, all_statuses=all_statuses, all_ressources=all_ressources_without_box)

@app.route("/<int:warehouse_id>/deliveries/<int:delivery_id>/boxes/<int:box_id>/ressources")
@login_required
@service.userRolesRequired('<int>/deliveries/<int>/boxes/<int>/ressources')
def warehouse_ressources(box_id, warehouse_id, delivery_id):
    ressources = service.getRessourcesByBox(box_id)
    all_statuses = service.getAllStatuses()
    return render_template('ressources.html', ressources=ressources, boxes=boxes, box_id=box_id, warehouse_id=warehouse_id, delivery_id=delivery_id, all_statuses=all_statuses)



#routes for the local helper
@app.route("/select_location", methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('select_location')
def select_location():
    if request.method == 'POST':
        location_id = request.form['selected_location']
        return redirect(url_for('projects', location_id=location_id))

    locations = service.getDestinations()
    return render_template('select_location.html', locations=locations)

@app.route("/<int:location_id>/projects", methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('<int>/projects')
def projects(location_id):
    projects = service.getProjectByLocation(location_id)
    location = service.getLocationByID(location_id)

    for project in projects:
        project.deliveries_count = service.getDeliveriesCountByProject(project.id)
        project.boxes_count = service.getBoxCountByProject(project.id)

    return render_template('projects.html', projects=projects, location=location, location_id=location_id)

@app.route("/<int:location_id>/projects/<int:project_id>/deliveries")
@login_required
@service.userRolesRequired('<int>/projects/<int>/deliveries')
def deliveries(location_id, project_id):
    deliveries = service.getDeliveriesByProject(project_id)
    all_statuses = service.getAllStatuses()

    for delivery in deliveries:
        delivery.boxes_count = service.getBoxCountByDelivery(delivery.id)

    return render_template('deliveries.html', deliveries=deliveries, project_id=project_id, location_id=location_id, all_statuses=all_statuses)

@app.route("/<int:location_id>/projects/<int:project_id>/deliveries/<int:delivery_id>/boxes")
@login_required
@service.userRolesRequired('<int>/projects/<int>/deliveries/<int>/boxes')
def boxes(delivery_id, location_id, project_id):
    boxes = service.getBoxesByDelivery(delivery_id)
    all_statuses = service.getAllStatuses()
    return render_template('boxes.html', boxes=boxes, location_id=location_id, project_id=project_id, delivery_id=delivery_id, all_statuses=all_statuses)

@app.route("/<int:location_id>/projects/<int:project_id>/deliveries/<int:delivery_id>/boxes/<int:box_id>/ressources")
@login_required
@service.userRolesRequired('<int>/projects/<int>/deliveries/<int>/boxes/<int>/ressources')
def ressources(box_id, delivery_id, location_id, project_id):
    ressources = service.getRessourcesByBox(box_id)
    all_statuses = service.getAllStatuses()
    return render_template('ressources.html', ressources=ressources, boxes=boxes, box_id=box_id, location_id=location_id, project_id=project_id, delivery_id=delivery_id, all_statuses=all_statuses)




#All routes for the Admin Panel

@app.route("/admin", methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('admin')
def admin():
    return render_template('admin.html')

@app.route("/admin/add_role", methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('admin/add_role')
def add_role():
    error_role_exists = ""

    role_name = ""

    if request.method == 'POST':
        role_name = request.form['role_name']
        if not service.doesRoleExist(role_name):
            service.addRole(role_name)
            return render_template('admin.html')
        else:
            error_role_exists = "A role with this name already exists. See the above table"
    
    roles = service.getAllRoles()
    return render_template('add_role.html', roles=roles, prev_role_name=role_name, error_role_exists=error_role_exists)

@app.route("/admin/add_user", methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('admin/add_user')
def add_user():
    error_username = ""
    error_password = ""

    firstname = ""
    lastname = ""
    username = ""
    password = ""
    confirm_password = ""
    role_id = ""

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role_id = request.form['role_id']

        usernameTaken = service.doesUserExist(username)
        if usernameTaken:
            error_username = 'This username is already taken.'
        if password != confirm_password:
            error_password = 'The passwords do not match.'
        if not error_username and not error_password:
            service.addUser(firstname=firstname, lastname=lastname, username=username, password=password, role_id=role_id)
            return render_template('admin.html')
    roles = service.getAllRoles()
    return render_template('add_user.html', prev_firstname=firstname, prev_lastname=lastname, prev_username=username, prev_password=password, prev_confirm_password=confirm_password, prev_role_id=role_id, roles=roles, error_username=error_username, error_password=error_password)

@app.route("/admin/delete_role", methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('admin/delete_role')
def delete_role():
    role_id = ""

    if request.method == 'POST':
        role_id = request.form['role_id']
        service.deleteRole(role_id)
        return render_template('admin.html')
    
    roles = service.getAllRoles()
    return render_template('delete_role.html', roles=roles)

@app.route("/admin/delete_user", methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('admin/delete_user')
def delete_user():
    user_id = ""

    if request.method == 'POST':
        user_id = request.form['user_id']
        service.deleteUser(user_id)
        return render_template('admin.html')
    
    users = service.getAllUsers()
    return render_template('delete_user.html', users=users)

@app.route("/admin/edit_user", methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('admin/edit_user')
def edit_user():
    error_same_role = ""
    error_unidentical_passwords = ""
    error_same_password = ""

    user_id = ""
    new_password = ""
    confirm_new_password = ""
    new_role_id = ""

    if request.method == 'POST':
        user_id = request.form['user_id']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
        new_role_id = request.form['new_role_id']

        # Was a new password entered?
        if confirm_new_password or new_password:
            # Were the entered passwords identical?
            if confirm_new_password != new_password:
                error_unidentical_passwords = "The passwords do not match."
            # Is the new password the same as the old one?
            elif service.doesUserHavePassword(user_id, new_password):
                error_same_password = "The new password must not equal the old one."
        # If no new password was assigned and the 'new role' is the same as the current one, no changes were made. so give an error
        elif service.doesUserHaveRole(user_id, new_role_id):
            error_same_role = "The user alrady has this role assigned to him"

        if not error_unidentical_passwords and not error_same_password and not error_same_role:
            service.setUserRole(user_id, new_role_id)
            # Only set the new password if it is not empty
            if new_password:
                service.setUserPassword(user_id, new_password)
            return render_template('admin.html')

    roles = service.getAllRoles()
    users = service.getAllUsers()
    return render_template('edit_user.html', users=users, roles=roles, prev_user_id=user_id, prev_new_password=new_password, prev_confirm_new_password=confirm_new_password, prev_role_id=new_role_id, error_unidentical_passwords=error_unidentical_passwords, error_same_password=error_same_password, error_same_role=error_same_role)


@app.route('/admin/routes', methods=['GET', 'POST'])
@login_required
@service.userRolesRequired('admin/routes')
def routes():
    roles = service.getAllRoles()
    permissions = service.getAllPermissions()

    if request.method == 'POST':
        for role in roles:
            for permission in permissions:
                permission_key = f"{role.id}_{permission.id}"
                has_permission = permission_key in request.form.getlist('permissions')
                if has_permission:
                    service.addRolePermission(role.id, permission.id)
                else:
                    service.deleteRolePermission(role.id, permission.id)

        return render_template('admin.html')

    role_permission_mapping = {}
    for role in roles:
        permission_mapping = {}
        for permission in permissions:
            role_permission = service.getRolePermission(role.id, permission.id)
            permission_mapping[permission.id] = role_permission is not None
        role_permission_mapping[role.id] = permission_mapping

    return render_template('routes.html', roles=roles, permissions=permissions, role_permission_mapping=role_permission_mapping)


#api functions

@app.route("/update_delivery_status/<int:delivery_id>", methods=['POST'])
def update_delivery_status(delivery_id):
    if request.method == 'POST':
        new_status_id = request.json.get('statusId')
        service.updateDeliveryStatus(delivery_id, new_status_id)

        return "Delivery status updated successfully"


@app.route("/update_box_status/<int:box_id>", methods=['POST'])
def update_box_status(box_id):
    if request.method == 'POST':
        status_id = request.json['statusId']
        service.updateBoxStatus(box_id, status_id)
        return "Box status updated successfully"


@app.route("/update_ressource_status/<int:ressource_id>", methods=['POST'])
def update_ressource_status(ressource_id):
    if request.method == 'POST':
        status_id = request.json['statusId']
        service.updateRessourceStatus(ressource_id, status_id)
        return "Ressource status updated successfully"

@app.route("/update_resource_amount/<int:resource_id>", methods=['POST'])
def update_resource_amount(resource_id):
    if request.method == 'POST':
        new_amount = request.json.get('amount')
        service.updateResourceAmount(resource_id, new_amount)

        return "Resource amount updated successfully"

service.checkRoutesInDataseAndInsert(app)
service.addDefaultRolePerm()

if __name__ == "__main__":
    app.run(debug=True)
