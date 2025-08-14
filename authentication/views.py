from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
import re
from django.conf import settings
from authentication.models import Coordinator, Faculty, Group

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username'].strip().lower()
        password = request.POST['password'].strip()

        user = User.objects.get(username=username)

        if user:
            user = authenticate(request, username=username, password=password)
            if user and user.first_name == 'Faculty':
                login(request, user)
                messages.success(request, 'Hurray! You\'re now logged in as !'+user.first_name)
                return redirect('fhome')
            elif user and user.first_name == 'Student':
                login(request, user)
                messages.success(request, 'Hurray! You\'re now logged in as !'+user.first_name)
                return redirect('shome')
            elif user and user.first_name == 'Admin':
                login(request, user)
                messages.success(request, 'Hurray! You\'re now logged in as !'+user.first_name)
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    return render(request, 'login.html')

def registerView(request):
    if request.method == 'POST':
        email = request.POST['email'].strip().lower()
        password = request.POST['password'].strip()
        confirm_password = request.POST['confirm_password'].strip()
        prn = request.POST['prn'].strip()
        name = request.POST['name'].strip().lower()
        key = request.POST['secret_key'].strip().upper()
        div = request.POST['div'].strip()
        dept = request.POST['dept'].strip()
        group_id = request.POST['group_id'].strip()
        roll = request.POST['roll_no'].strip()
        contact_num = request.POST['contact_num'].strip()
        errors = {}

        # Validating email
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "Invalid email format."

        # PRN validation (must be 8 digits)
        if not prn.isdigit() or (prn != '0' and len(prn) != 8):
            errors['prn'] = "PRN must be 8 digits."
        
        if not roll.isdigit() or (roll != '0' and len(roll) > 2):
            errors['roll'] = "Roll number must be at most 2 digits."

        if not contact_num.isdigit() or len(contact_num) != 10:
            errors['contact_num'] = "Contact number must be 10 digits."

        if not div:
            errors['div'] = "Division is required."

        if not dept:
            errors['dept'] = "Department is required."

        if not group_id.isdigit() or len(group_id) > 2:
            errors['group_id'] = "Invalid group ID. You only need to enter your group number."

        # Password validation
        password_regex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        if password != confirm_password:
            errors['password'] = "Passwords do not match."
        elif not password_regex.match(password):
            errors['password'] = ("Password must be at least 8 characters long, "
                                  "include one uppercase letter, one lowercase letter, "
                                  "one digit, and one special character.")

        # Checking if the PRN already exists
        if User.objects.filter(username=prn).exists():
            errors['prn'] = "PRN already exists."

        # Checking for required fields
        required_fields = ['email', 'password', 'confirm_password', 'prn', 'name']
        for field in required_fields:
            if not request.POST.get(field):
                errors[field] = f"{field.replace('_', ' ').capitalize()} is required."

        # Checking if the secret key is correct
        if key == settings.FACULTY_KEY:
            role = 'Faculty'
        elif key == settings.STUDENT_KEY:
            role = 'Student'
        elif key == settings.ADMIN_KEY:
            role = 'Admin'
        else:
            role = None
            errors['secret_key'] = "Invalid secret key."

        # If any errors found
        if errors:
            return render(request, 'register.html', {'errors': errors, 'form_data': request.POST})

        # If no errors, creating the user
        user = User.objects.create_user(username=email, password=password, first_name=role, last_name=name, email=email)
        user.save()

        if role == 'Student':
            Group.objects.create(sname=name, email=email, dept=dept, div=div, prn=prn, group_id=dept+'-'+group_id, roll=roll, contact_num=contact_num)
        elif role == 'Faculty':
            Faculty.objects.create(fname=name, email=email, dept=dept, contact_num=contact_num)
        elif role == 'Admin':
            Coordinator.objects.create(cname=name, email=email, dept=dept, contact_num=contact_num)

        messages.success(request, 'User created successfully')
        return redirect('login')

    return render(request, 'register.html')

def logoutView(request):
    logout(request)
    return redirect('login')
