from django.urls import path
from . import views

urlpatterns = [
        # path('', views.dashboard, name = 'dashboard'),
		# path('', views.index, name = 'home'),
        # path('withdrawal/', views.withdrawal, name = 'withdrawal'),
        path('tutor_signup/', views.tutor_signup, name="tutor_signup"),
		path('tutor_login/', views.tutor_login, name="tutor_login"),


        

    	path('account_settings/', views.account_settings, name="saler_account_settings"),
        path('student_dashboard/',views.studentDashboard,name="studentDashboard"),


        # studdent dashboard
        path("student_bookings",views.studentBookings,name="studentBookings"),
        path("student_profile",views.studentProfile,name="studentProfile"),


    #  admin dashboard
        path("updateProfile/",views.updateProfile,name="updateProfile"),
        path("logout_tutor",views.logout_tutor,name="logout_tutor"),
        path("processUpdateForm",views.updateProfileForm,name="updatProfileForm"),
        path("addSkill",views.addSkill,name="addSkill"),
        path("addTutorSkillsForm",views.addTutorSkillsForm,name="addTutorSkillsForm"),
        path("addTimeSlot/<str:skill_id>",views.addTimeSlot,name="addTimeSlot"),
        path("addTimeSlotForm/<str:skill_id>",views.addTimeSlotForm,name="addTimeSlotForm"),
        path('update_booking_status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
        path("bookings",views.staffBookings,name="staffBookings"),
        path("withdrawals",views.withdrawals,name="withdrawals"),
        path("reviews",views.reviews,name="reviews"),
        
        
        # booking
        path("tutor_profile/<str:tutor_id>",views.tutor_profile,name="tutor_profile"),
        path("bookSession/<str:tutor_id>",views.bookSession,name="bookSession"),
        path("rate_tutor/<str:tutor_id>",views.rateTutor,name="rateTutor"),
        
        
        # payments
        path("getAuthToken",views.getAuthToken,name="getAuthToken"),
        path("registerIpnUrl",views.registerIpnUrl,name="registerIpnUrl"),
        path("submitOrder",views.submitOrder,name="submitOrder"),
            

    	path('add_product/', views.add_product, name="add_product"),
    	path('view_products/', views.view_products, name="view_products"),
    	path('plus_element_cart/', views.plus_element_cart),
    	path('minus_element_cart/', views.minus_element_cart),
    	path('add_to_cart/', views.add_to_cart),
    	path('delete_from_cart/', views.delete_from_cart),
        path('cart/', views.mycart, name="cart"),
    	path('MyOrders/', views.MyOrders, name="seller_orders"),
    	path("products/<str:catg>", views.view_all, name="saler_products_view_all"),
    	path("product/<int:prod_id>", views.productView, name="SalerProductView"),
    	path("checkout/", views.checkout, name = "checkout")
	]