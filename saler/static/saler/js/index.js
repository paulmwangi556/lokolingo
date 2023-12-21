$(document).ready(function () {
$(".update_booking").click(function(){
    showBookingForm();
});
    
    
});

function showBookingForm(){
    var form = $(".bookings-form");
    form.toggle()

}