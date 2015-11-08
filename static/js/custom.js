$(function(){
    $('.submit').on('submit',function(event){
       event.preventDefault() ;
       event.stopPropagation();
       alert("Form Submission prevented / stoped.");
    });
});