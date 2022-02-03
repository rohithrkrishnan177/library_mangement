from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User,BookModel, IssueBook, ReturnBook, Student

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username')

admin.site.register(User, UserAdmin)


class Student_Admin(admin.ModelAdmin):
    list_display = ("id", "user_id", "student_name", "phone")


admin.site.register(Student, Student_Admin)


class BookModel_admin(admin.ModelAdmin):
    list_display = ("id", "user_addbook", "bookname", "subject", "quantity")


admin.site.register(BookModel, BookModel_admin)


class IssueBookAdmin(admin.ModelAdmin):
    list_display = ("id", "user_issuebook", "bookid2", "current_date", "expiry_date")


admin.site.register(IssueBook, IssueBookAdmin)


class ReturnBookAdmin(admin.ModelAdmin):
    list_display = ("id", "user_returnbook", "issuebook_id")


admin.site.register(ReturnBook, ReturnBookAdmin)
