import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { Router } from '@angular/router';
import { NgxSpinnerService } from "ngx-spinner"; 
import { ToastrService } from 'ngx-toastr';
import { User } from 'src/app/models/user';
import { ActivatedRoute } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  id:any = '';
  user: User = new User();
  password: string = "";
  password2: string = "";
  register: boolean = false;

  constructor(
    private activatedRoute: ActivatedRoute,
    private authService: AuthService,
    private router: Router,
    private SpinnerService: NgxSpinnerService,
    private toastr: ToastrService,
    private cookieService: CookieService,
  ) {
  }

  ngOnInit(): void {
    this.id = this.activatedRoute.snapshot.paramMap.get('id');
    if (this.id === undefined || this.id == '') {
      this.router.navigate(['/']);
    }
    else if (this.id == "new"){
      this.register = true;
    }
    else{
      this.SpinnerService.show();
      this.authService.getUser(this.id).subscribe(
        data => {
          this.user = data;
          this.SpinnerService.hide();
        },
        error => {
          this.toastr.error(error.message, 'Error!');
          this.SpinnerService.hide();
        }
      );
    }
  }

  onSubmit(){
    window.scroll(0,0);
    this.SpinnerService.show();
    if(this.register){
      this.user.password = this.password;
      this.authService.register(this.user).subscribe(
        data => {
          console.log(data);
          this.SpinnerService.hide();
          this.toastr.success('Register succesfull', 'Successfull!');
          this.router.navigate(['/']);
        },
        error => {
          this.toastr.error(error.error.error, 'Error!');
          this.SpinnerService.hide();
        }
      );
    }
    else{
      if(this.password != '' && this.password == this.password2){
        this.user.password = this.password;
      }
      this.authService.updateUser(this.user).subscribe(
        data => {
          this.SpinnerService.hide();
          this.toastr.success('Update succesfull', 'Successfull!');
          this.router.navigate(['/']);
        },
        error => {
          this.toastr.error(error.error.error, 'Error!');
          this.SpinnerService.hide();
        }
      );
    }
  }

  deleteUser(){
    if (window.confirm("Are you sure you want to delete this user permanently?")) {
      window.scroll(0,0);
      this.SpinnerService.show();
      this.authService.deleteUser(this.id).subscribe(
        data => {
          this.cookieService.delete("userId");
          this.SpinnerService.hide();
          this.toastr.success('Delete succesfull', 'Successfull!');
          window.location.reload();
        },
        error => {
          this.toastr.error(error.message, 'Error!');
          this.SpinnerService.hide();
        }
      );
    }
  }
}
