    <!--for-fixed-hedder-->
$(window).scroll(function() {
	 
    if ($(this).scrollTop() > 50){  
        $('#myHeader').addClass("content_fixed");
    }
    else{
        $('#myHeader').removeClass("content_fixed");
    }
});