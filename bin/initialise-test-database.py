from django.contrib.auth.models import User
from carnique.profile.models    import UserProfile
from carnique.news.models       import News
from carnique.quotes.models     import Quote

from django.contrib.auth.hashers import make_password

def run():
    empty_data()
    add_data()

def empty_data():
    for u in User.objects.all():
        u.delete()

    for n in News.objects.all():
        n.delete()

    for q in Quote.objects.all():
        q.delete()


def add_data(): 
    u_test = User(
        username="testuser",
        first_name="Jan",
        last_name="Tester",
        password=make_password("testuser"),
    )
    u_test.save()
    up = UserProfile(
        user=u_test,
        is_member=True,
    )
    up.save()

    u_admin = User(
        username="adminuser",
        first_name="Sten",
        last_name="Admin",
        password=make_password("adminuser"),
    )
    u_admin.save()
    up = UserProfile(
        user=u_admin,
        is_member=True,
    )
    up.save()

    n = News(
        title = "Dit is nieuws",
        text = "En dit is de omschrijving",
        added_by = u_admin,
    )
    n.save()

    q1 = Quote(
        title="Zo hoort het!",
        text="<Habbie> wat een kniesoor\n<Domilijn> Gezondheid!",
        added_by=u_test,
    )
    q1.save()

    q2 = Quote(
        title="Grote jongen",
        text="12:31 < RS-232> Emphyrio: dan nee dank je. ik heb 11\" en wil dat formaat graag houden.",
        added_by=u_test,
    )
    q2.save()

run()
