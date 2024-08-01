from django.shortcuts import render, redirect            
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

#Login
def login_view(request):
    #error_message to None                                 
    error_message = None
    #create a Form object 
    form = AuthenticationForm()

    #when user hits "login" button, then POST request is generated
    if request.method == 'POST':       
        #read the data sent by the form via POST request                   
        form =AuthenticationForm(data=request.POST)

        #check if form is valid
        if form.is_valid():                                
            username=form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user=authenticate(username=username, password=password)
            if user is not None:                    
            #if user is authenticated use Django function to login
                login(request, user)
                #send the user to desired page             
                return redirect('recipes:list')
            
            else:
                error_message = "Sorry, it seems something has gone wrong."

    context ={                                             
        'form': form,
        'error_message': error_message
   }
    #load the login page using "context" information
    return render(request, 'auth/login.html', context)


#Logout
def logout_view(request):                                  
    #Use Django function to logout
    logout(request)  
    #After logging out send to login form (or generic page) 
    return render(request, 'auth/success.html')

