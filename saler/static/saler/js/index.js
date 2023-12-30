// $(document).ready(function () {
 
    
// });

function triggerBtn(button){
    // console.log(button)
    // var elements = $('.bookings-form');
    $(".update_booking").click(function(){
        // showBookingForm();
        console.log(button)
        var index = button-1;
        var form = $('.bookings-form:eq(' + index +')');
        form.toggle()
      
        

    });
       
}

function showBookingForm(){
    var form = $(".bookings-form");
    form.toggle()

}