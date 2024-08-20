

   

    document.getElementById('show-password').addEventListener('change', function(){
        var passwordField = document.getElementById('passwordField');
        if (this.checked){
            passwordField.type ='text';
        }else{
            passwordField.type ='password';
        }
    });



    setTimeout(function(){
        $('#message').fadeOut('slow')
      }, 4000)