import uuid

from OrmMetadata.Classes import *

from OrmMetadata.Box import *
from OrmMetadata.Category import *
from OrmMetadata.Content import *
from OrmMetadata.Delivery import *
from OrmMetadata.Location import *
from OrmMetadata.Permission import *
from OrmMetadata.Project import *
from OrmMetadata.Ressource import *
from OrmMetadata.Role import *
from OrmMetadata.Status import *
from OrmMetadata.Unit import *
from OrmMetadata.User import *

from OrmMetadata.Project_Delivery import *
from OrmMetadata.Role_Perm import *

from instance.add_roles import *
from instance.add_role_perm import *

from functools import wraps
from flask import request, abort
from flask_login import current_user

import re

DBSession = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def createProject(project_name, location_name):
    session = DBSession()
    location = session.query(Location).filter_by(name=location_name).first()

    if not location:
        location = Location(name=location_name,is_warehouse=False)
        session.add(location)
        session.commit()

    new_project = Project(name=project_name, destination=location)
    session.add(new_project)
    session.commit()

def createDelivery(warehouse_id, status_name, arrival_date, project_id):
    session = Session()

    departure = session.query(Location).filter_by(id=warehouse_id).first()
    status = session.query(Status).filter_by(status=status_name).first()

    new_delivery = Delivery(
        departure_id=departure.id,
        status_id=status.id,
        arrival_date=arrival_date
    )

    session.add(new_delivery)

    session.flush()

    project_delivery = Project_Delivery(
        project_id=project_id,
        delivery_id=new_delivery.id
    )
    session.add(project_delivery)

    session.commit()

    return new_delivery.id

def getAllProjects():
    session = DBSession()   
    return session.query(Project).all()

def getAllDeliveries():
    session = DBSession()
    return session.query(Delivery).all()

def getDeliveriesByProject(project_id):
    session = DBSession()
    deliveries = session.query(Delivery) \
        .join(Project_Delivery, Delivery.id == Project_Delivery.delivery_id) \
        .join(Project, Project.id == Project_Delivery.project_id) \
        .join(Location, Location.id == Project.destination_id) \
        .filter(Project_Delivery.project_id == project_id) \
        .options(joinedload(Delivery.delivery_projects)) \
        .all()

    return deliveries

def getDeliveriesByDepature(warehouse_id):
    session = DBSession()
    deliveries = session.query(Delivery) \
        .filter_by(departure_id=warehouse_id) \
        .join(Project_Delivery, Delivery.id == Project_Delivery.delivery_id) \
        .join(Project, Project.id == Project_Delivery.project_id) \
        .join(Location, Location.id == Project.destination_id) \
        .all()
    return deliveries

def getDeliveriesCountByProject(project_id):
    session = DBSession()
    deliveries_count = session.query(func.count(Project_Delivery.delivery_id)).filter_by(project_id=project_id).scalar()
    return deliveries_count

def getBoxCountByProject(project_id):
    session = DBSession()
    box_count = session.query(func.count(Box.id)).join(Delivery).join(Project_Delivery).filter(Project_Delivery.project_id == project_id).scalar()
    return box_count

def getBoxCountByDelivery(delivery_id):
    session = DBSession()
    box_count = session.query(func.count(Box.id)).filter_by(delivery_id=delivery_id).scalar()
    return box_count

def getAllBoxes():
    session = DBSession()
    return session.query(Box).all()

def getBoxesByDelivery(delivery_id):
    session = DBSession()
    boxes = session.query(Box).options(joinedload(Box.category), joinedload(Box.status), joinedload(Box.delivery)).filter_by(delivery_id=delivery_id).all()
    return boxes
    session.close()

def createBox(category_name, status_name, box_description, delivery_id):
    session = DBSession()

    # Suchen der Kategorie und des Status
    category = session.query(Category).filter_by(category=category_name).first()
    status = session.query(Status).filter_by(status=status_name).first()

    # Erstellen einer neuen Box
    new_box = Box(
        category_id=category.id,
        status_id=status.id,
        delivery_id=delivery_id,
        description=box_description
    )

    session.add(new_box)
    session.commit()

    return new_box.id


def updateBoxIdRessource(box_id, resource_ids):
    session = DBSession()

    for resource_id in resource_ids:
        resource = session.query(Ressource).get(resource_id)
        resource.box_id = box_id

    session.commit()

def getWarehouses():
    session = DBSession()
    locations = session.query(Location).filter(Location.is_warehouse == True).all()
    return locations

def getAllLocations():
    session = DBSession()
    return session.query(Location).all()

def getDestinations():
    session = DBSession()
    locations = session.query(Location).filter(Location.is_warehouse == False).all()
    return locations

def getLocationByID(locationID):
    session = DBSession()
    return session.query(Location).filter_by(id=locationID).all()

def getProjectByLocation(locationID):
    session = DBSession()
    projects = session.query(Project).options(joinedload(Project.destination)).filter_by(destination_id=locationID).all()
    return projects

def getAllStatuses():
    session = DBSession()   
    return session.query(Status).all()

def getAllCategories():
    session = DBSession()
    return session.query(Category).all()

def getAllRessources():
    session = DBSession()
    return session.query(Ressource).all()


def getRessourcesByBox(box_id):
    session = DBSession()
    boxes = session.query(Ressource).filter_by(box_id=box_id).all()
    return boxes

def getRessourcesWithoutBox():
    session = DBSession()
    boxes = session.query(Ressource).filter(Ressource.box_id == None).all()
    return boxes


def checkLoginUser(username, password):
    session = DBSession()   
    return session.query(User).filter_by(username=username, password=password).first()

# Fetches all roles from the DB and returns them
def getAllRoles():
    session = DBSession()   
    return session.query(Role).all()

def getAllPermissions():
    session = DBSession()
    return session.query(Permission).all()

def getRolePermission(role_id, permission_id):
    session = DBSession()
    return session.query(Role_Perm).filter_by(role_id=role_id, permission_id=permission_id).first()


def addRolePermission(role_id, permission_id):
    session = DBSession()
    existing_role_permission = session.query(Role_Perm).filter_by(role_id=role_id, permission_id=permission_id).first()

    if existing_role_permission is None:
        new_role_permission = Role_Perm(role_id=role_id, permission_id=permission_id)
        session.add(new_role_permission)
        session.commit()

def deleteRolePermission(role_id, permission_id):
    session = DBSession()
    role_permission = session.query(Role_Perm).filter_by(role_id=role_id, permission_id=permission_id).first()
    if role_permission:
        session.expunge(role_permission)
        session.delete(role_permission)
        session.commit()

# Checks whether or not username is already taken
def doesUserExist(username):
    session = DBSession()
    user = session.query(User).filter_by(username=username).first()
    return True if user else False

# Adds a new user
def addUser(firstname, lastname, username, password, role_id):
    new_user = User(surname=firstname, name=lastname, username=username, password=password, role_id=role_id)
    session = DBSession()   
    session.add(new_user)
    session.commit()

# Fetches all users from the DB and returns them
def getAllUsers():
    session = DBSession()   
    return session.query(User).all()

# Checks whether or not a given user already has the given role assigned to him
def doesUserHaveRole(user_id, role_id):
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).first()
    return True if user.role_id == int(role_id) else False

# Checks whether or not a given user already has the given password as their current one
def doesUserHavePassword(user_id, password):
    session = DBSession()
    user = session.query(User).filter_by(id=user_id, password=password).first()
    return True if user else False

# Sets the Role of the given user
def setUserRole(user_id, role_id):
    session = DBSession()
    user = session.query(User).get(user_id)
    user.role_id = role_id
    session.commit()

# Sets the Password 
def setUserPassword(user_id, password):
    session = DBSession()
    user = session.query(User).get(user_id)
    user.password = password
    session.commit()

# Deletes a given user
def deleteUser(user_id):
    session = DBSession()
    user = session.query(User).get(user_id)
    session.delete(user)
    session.commit()

# Adds a new role
def addRole(role_name):
    new_role = Role(name=role_name)
    session = DBSession()
    session.add(new_role)
    session.commit()

# Checks whether or not a role already exists
def doesRoleExist(role_name):
    session = DBSession()
    role = session.query(Role).filter_by(name=role_name).first()
    return True if role else False

# Deletes a given role
def deleteRole(role_id):
    session = DBSession()
    role = session.query(Role).get(role_id)
    session.delete(role)
    session.commit()



#api services

def updateDeliveryStatus(delivery_id, new_status_id):
    session = DBSession()
    delivery = session.query(Delivery).filter_by(id=delivery_id).first()
    new_status = session.query(Status).filter_by(id=new_status_id).first()
    delivery.status = new_status

    session.commit()


def updateBoxStatus(box_id, status_id):
    session = DBSession()
    box = session.query(Box).filter_by(id=box_id).first()
    box.status_id = status_id

    session.commit()

def updateResourceAmount(resource_id, new_amount):
    session = DBSession()
    resource = session.query(Ressource).filter_by(id=resource_id).first()
    resource.amount = new_amount

    session.commit()

def updateRessourceStatus(ressource_id, status_id):
    session = DBSession()
    ressource = session.query(Ressource).filter_by(id=ressource_id).first()
    if ressource is None:
        return "Ressource not found"
    ressource.status_id = status_id

    session.commit()


def userRolesRequired(endpoint):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated:
                route_path = request.path

                print(f"Checking permission for route: {route_path}")

                user_role = dbsession.query(Role).get(current_user.role_id)
                if user_role:
                    role_routes = user_role.permissions

                    for role_route in role_routes:
                        pattern = re.escape(role_route.name)
                        pattern = re.sub(r'<[^>]+>', r'.*', pattern)
                        if re.fullmatch(pattern, route_path):
                            return fn(*args, **kwargs)
                    print("Permission denied.")
                    abort(403)
                else:
                    print("User's role not found.")
                    abort(403)
            else:
                print("Not authenticated.")
                abort(401)

        return decorated_view

    return wrapper


def checkPermission(user, endpoint):
    if user.role_id:
        role = dbsession.query(Role).get(user.role_id)
        if role:
            route = dbsession.query(Permission).filter_by(name=endpoint).first()
            if route:
                return True
            else:
                pattern = re.sub(r'<[^>]+>', r'.*', endpoint)
                matching_route = dbsession.query(Permission).filter_by(name=pattern).first()
                if matching_route:
                    role_route = dbsession.query(Role_Perm).filter_by(role_id=role.id, permission_id=matching_route.id).first()
                    return role_route is not None
    return False


def checkRoutesInDataseAndInsert(app):
    existing_routes = dbsession.query(Permission).all()
    existing_route_names = {route.name for route in existing_routes}


    current_routes = {rule.rule for rule in app.url_map._rules if rule.endpoint not in ['static']}


    new_routes = current_routes - existing_route_names
    new_route_objects = [Permission(name=route) for route in new_routes]
    dbsession.bulk_save_objects(new_route_objects)


    routes_to_delete = [route for route in existing_routes if route.name not in current_routes]
    for route in routes_to_delete:
        dbsession.delete(route)


    for role_data in default_roles:
        role_name = role_data['name']
        if not dbsession.query(exists().where(Role.name == role_name)).scalar():
            role = Role(name=role_name)
            dbsession.add(role)

    dbsession.commit()


    admin_role = dbsession.query(Role).filter_by(name='admin').first()
    if admin_role:
        existing_role_routes = dbsession.query(Role_Perm).filter_by(role_id=admin_role.id).all()
        existing_route_ids = {role_route.permission_id for role_route in existing_role_routes}

        routes = dbsession.query(Permission).filter(Permission.id.notin_(existing_route_ids)).all()
        for route in routes:
            admin_role.permissions.append(route)

        dbsession.commit()


def addDefaultRolePerm():
    session = DBSession()
    for entry in data:
        role_perm_entry = Role_Perm(**entry)
        existing_entry = session.query(Role_Perm).filter_by(role_id=entry['role_id'], permission_id=entry['permission_id']).first()
        if existing_entry is None:
            session.add(role_perm_entry)
            session.commit()