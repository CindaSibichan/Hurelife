from django.urls import path,include
from . views import *
 

urlpatterns = [


    # view profiles
    path('p-profile/<int:pk>/',PatientProfileView.as_view() , name="p-profile"),
    path('d-profile/<int:pk>/',DoctorProfileView.as_view() , name="d-profile"),

    # edit profiles
    path('d-editprofile/<int:pk>/',DoctorEditProfileView.as_view() ,name="d-editprofile" ),
    path('p-editprofile/<int:pk>/',PatientEditProfileView.as_view() , name="p-ditprofile"),

    # list all doctors and patients
    path('listdoctor/',ListAllDoctorsView.as_view(), name="listdoctor"),
    path('listpatient/',ListAllPatientsView.as_view() , name="listpatient"),

    # list doctor by specialize
    path('list-docbyspecia/',ListDoctorBySpecialize.as_view (), name="list-docspecia"),
    
    # doctor appoinment planning
    path('doc-plan/',DoctorAvailabilityView.as_view() , name="doc-plan"),
    path('docplan-list/',ListDoctorAvailability.as_view() , name="docplan-list"),
    path('delete-plan/<id>/',DeleteDoctorAvailability.as_view() , name="delete-plan"),

    #Book apointment 
    path('book-appointment/' ,BookAppointment.as_view() , name="book-appointment" ),
    path('payment/',AppointmentPaymentView.as_view(), name ="payment"),
    path('list-appointment/',ListAppointments.as_view() , name="list-appointment"),
    path('delete-appointment/<id>/',DeleteAppointments.as_view() , name="delete-appointment"),


    path('offline-pay/',SetOfflineChatView.as_view() ,name = 'offline-pay'),
    #recent appointments
    path('recent-appointments/',RecentAppointments.as_view() , name="recent-appointments"),
    # upcoming appointments
    path('upcoming-appointments/' ,UpcomingAppointments.as_view() , name="upcoming-appointments" ),

    #appointments for doctors
    path('upcomingappoint-for-doc/<int:doctor_id>/',UpcomingAppointmentForDoctor.as_view() , name = "appointment-for-doc")


    
]