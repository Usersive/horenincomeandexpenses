

   

    // document.getElementById('show-password').addEventListener('change', function(){
    //     var passwordField = document.getElementById('passwordField');
    //     if (this.checked){
    //         passwordField.type ='text';
    //     }else{
    //         passwordField.type ='password';
    //     }
    // });



    

        // document.getElementById('toggle-password').addEventListener('click', function() {
        //     var passwordInput = document.getElementById('password');
        //     var togglePassword = document.getElementById('toggle-password');
        //     if (passwordInput.type === 'password') {
        //         passwordInput.type = 'text';
        //         togglePassword.textContent = '🙈'; 
        //     } else {
        //         passwordInput.type = 'password';
        //         togglePassword.textContent = '👁'; 
        //     }
        // });
 

        function password_show_hide() {
            var x = document.getElementById("password");
            var show_eye = document.getElementById("show_eye");
            var hide_eye = document.getElementById("hide_eye");
            hide_eye.classList.remove("d-none");
            if (x.type === "password") {
              x.type = "text";
              show_eye.style.display = "none";
              hide_eye.style.display = "block";
            } else {
              x.type = "password";
              show_eye.style.display = "block";
              hide_eye.style.display = "none";
                }
          }
        
          function password2_show_hide() {
            var x = document.getElementById("password2");
            var show_eye = document.getElementById("show_eye2");
            var hide_eye = document.getElementById("hide_eye2");
            hide_eye.classList.remove("d-none");
            if (x.type === "password") {
              x.type = "text";
              show_eye.style.display = "none";
              hide_eye.style.display = "block";
            } else {
              x.type = "password";
              show_eye.style.display = "block";
              hide_eye.style.display = "none";
                }
          }



    setTimeout(function(){
        $('#message').fadeOut('slow')
      }, 4000)






      setTimeout(function(){
        $('#message').fadeOut('slow')
      }, 4000)