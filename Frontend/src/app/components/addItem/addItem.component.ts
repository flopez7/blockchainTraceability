import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { Router } from '@angular/router';
import { NgxSpinnerService } from "ngx-spinner"; 
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-addItem',
  templateUrl: './addItem.component.html',
  styleUrls: ['./addItem.component.css']
})
export class AddItemComponent implements OnInit {

  name: string = '';
  place: string = '';
  description: string = '';

  constructor(
    private apiService: ApiService,
    private router: Router,
    private SpinnerService: NgxSpinnerService,
    private toastr: ToastrService
  ) { }

  ngOnInit() {
  }

  onSubmit(){
    window.scroll(0,0);
    this.SpinnerService.show(); 
    this.apiService.addItem(this.name,this.place,this.description).subscribe(
      data => {      
        this.SpinnerService.hide();
        this.router.navigate(['/editItem/'+data.id]);
      },
      error => {
        this.toastr.error(error.message, 'Error!');
        this.SpinnerService.hide();
      }
    );
  }

}
