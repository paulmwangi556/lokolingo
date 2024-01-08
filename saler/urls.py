from django.urls import path
from . import views

urlpatterns = [
        # path('', views.dashboard, name = 'dashboard'),
		# path('', views.index, name = 'home'),
        # path('withdrawal/', views.withdrawal, name = 'withdrawal'),
        path('tutor_signup/', views.tutor_signup, name="tutor_signup"),
		path('tutor_login/<path:next_page>/', views.tutor_login, name="tutor_login"),


        

    	path('account_settings/', views.account_settings, name="saler_account_settings"),
        path('student_dashboard/',views.studentDashboard,name="studentDashboard"),


        # studdent dashboard
        path("student_bookings",views.studentBookings,name="studentBookings"),
        path("student_courses",views.studentCourses,name="studentCourses"),
        path("student_profile",views.studentProfile,name="studentProfile"),
        path("updateStudentProfileForm",views.updateStudentProfile,name="updateStudentProfileForm"),
        path("studentTransactionHistory",views.checkTransactionHistory,name="studentTransactionHistory"),


    #  admin dashboard
        path("updateProfile/",views.updateProfile,name="updateProfile"),
        # path("updateProfileForm/",views.updateProfileForm,name="updateProfileForm"),
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
        path("tutorSessions",views.tutorSessions,name="tutorSessions"),
        path("createSession/<str:booking_id>",views.createSession,name="createSession"),
        path("withdrawFundsForm",views.withdrawFundsForm,name="withdrawFundsForm"),
        path("cancelWithdrawRequest/<str:withdraw_id>",views.cancelWithdrawRequest,name="cancelWithdrawRequest"),
        path("courseManagement",views.courseManagement,name="courseManagement"),
        path("addCourse",views.addCourse,name="addCourse"),  
        path("adminCourse/<str:course_id>",views.courseDetails,name="adminCourse"),
        path("adminCourseResources/<str:course_id>",views.adminCourseResources,name="adminCourseResources"),
        path("addSectionResource/<str:section_id>/<str:course_id>",views.addSectionResource,name="addSectionResource"),
        path("deActivateProfile",views.deactivateProfile,name="deActivateProfile"),
        
        
        path("editSection/<str:section_id>",views.editSection,name="editSection"),
        path("deleteSection/<str:section_id>/<str:course_id>",views.deleteSection,name="deleteSection"),
        
        path("editResource/<str:resource_id>/<str:course_id>",views.editResource,name="editResource"),
        path("deleteResource/<str:resource_id>/<str:course_id>",views.deleteResource,name="deleteResource"),
        
        
        # booking
        path("tutor_profile/<str:tutor_id>",views.tutor_profile,name="tutor_profile"),
        path("bookSession/<str:tutor_id>",views.bookSession,name="bookSession"),
        path("rate_tutor/<str:tutor_id>",views.rateTutor,name="rateTutor"),
        
               
        # payments
        path("payments",views.payments,name="payments"),
        path("getAuthToken",views.getAuthToken,name="getAuthToken"),
        path("registerIpnUrl",views.registerIpnUrl,name="registerIpnUrl"),
        path("submitOrder/<str:booking_id>/<str:item>",views.submitOrder,name="submitOrder"),
        path("transaction_status/<str:order_tracking_id>",views.getTransactionStatus,name="transactionStatus"),
            
        # chat
        path("chat",views.chatView,name="chat"),
        path("studentChat/<str:tutor_id>",views.studentChat,name="studentChat"),
        
        path("staffChatRoom/<str:room_id>",views.staffChatRoom,name="staffChat"),
        path("chatRoom/<str:room_id>",views.chatRoom,name="chatRoom"),
        
        
        
        
        
        
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