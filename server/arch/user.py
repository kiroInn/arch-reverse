import flask
from arch.db.db_user import User

def index():
    # As a list to test debug toolbar
    User.objects().delete()  # Removes
    User(UserID=1, LogonNullity=True, UserRight="1", ManageRight="1", RegisterDate=dete.datetime.datetime().utcnow()).save()
    users = User.objects.all()
    return users

def pagination():
    User.objects().delete()
    for i in range(10):
        User(UserID=i, LogonNullity=True, UserRight="1", ManageRight="1", RegisterDate=dete.datetime.datetime().utcnow()).save()  # Insert

    page_num = int(flask.request.args.get('page') or 1)
    todos_page = User.objects.paginate(page=page_num, per_page=3)
    return

