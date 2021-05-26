import { Component, OnInit } from '@angular/core';
import { Item } from '../../models/item';
import { ApiService } from '../../services/api.service';
import { NgxSpinnerService } from "ngx-spinner"; 
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-items',
  templateUrl: './items.component.html',
  styleUrls: ['./items.component.css']
})
export class ItemsComponent implements OnInit {

  items: Item[] = [];

  constructor(
    private apiService: ApiService,
    private SpinnerService: NgxSpinnerService,
    private toastr: ToastrService
  ) { }

  ngOnInit() {
    this.SpinnerService.show(); 
    this.apiService.getItems().subscribe(
      data => {
        this.items = data;
        this.SpinnerService.hide();
      },
      error => {
        this.toastr.error(error.error.error, 'Error!');
        this.SpinnerService.hide();
      }
    );
  }

  deleteItem(item : Item){
    this.SpinnerService.show(); 
    this.apiService.deleteItem(item.id).subscribe(
      data => {
        this.items = data;
        this.SpinnerService.hide();
      },
      error => {
        this.toastr.error(error.message, 'Error!');
        this.SpinnerService.hide();
      }
    );
  }

}
