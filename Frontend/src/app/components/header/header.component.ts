import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  status: boolean = this.cookieService.check("userId");
  userId: string = this.cookieService.get("userId");

  constructor(private cookieService: CookieService, private router: Router) { }

  ngOnInit(): void {
  }

  logout(){
    this.cookieService.delete("userId");
    window.location.reload()
  }

  redirectTo(uri:string){
    this.router.navigateByUrl('/', {skipLocationChange: true}).then(()=>
    this.router.navigate([uri]));
 }
}
