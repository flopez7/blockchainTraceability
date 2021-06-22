import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { Router } from '@angular/router';
import { NgxSpinnerService } from "ngx-spinner"; 
import { ToastrService } from 'ngx-toastr';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  username: string = "";
  password: string = "";

  constructor(
    private authService: AuthService,
    private router: Router,
    private SpinnerService: NgxSpinnerService,
    private toastr: ToastrService,
    private cookieService: CookieService,
  ) { }

  ngOnInit() {
    if(this.cookieService.check('userId')){
      this.router.navigate(['/']);
    }
  }

  onSubmit(){
    this.SpinnerService.show(); 
    this.authService.login(this.username,this.password).subscribe(
      data => {
        this.SpinnerService.hide();
        if(data.result == "true"){
          this.toastr.success('Login succesfull', 'Successfull!');
          this.router.navigate(['/']);
          window.location.reload()
          this.cookieService.set('userId', this.username, 1, '/');
        }else{
          this.toastr.error('Incorrect password', 'Error!');
        }
      },
      error => {
        this.toastr.error(error.error.error, 'Error!');
        this.SpinnerService.hide();
      }
    );
  }
}
