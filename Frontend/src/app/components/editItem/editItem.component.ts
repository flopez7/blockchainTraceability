import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Item } from 'src/app/models/item';
import { ApiService } from '../../services/api.service';
import { NgxSpinnerService } from "ngx-spinner"; 
import { ToastrService } from 'ngx-toastr';
import {NgbModal, ModalDismissReasons, NgbModalOptions} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-editItem',
  templateUrl: './editItem.component.html',
  styleUrls: ['./editItem.component.css']
})
export class EditItemComponent implements OnInit {

  id:any = '';
  item: Item = new Item();
  newPlace : string = '';
  newDescription : string = '';
  source: Item = new Item();
  derived: Item[] = [];
  

  closeResult: string = "";
  modalOptions:NgbModalOptions;
  
  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private apiService: ApiService,
    private SpinnerService: NgxSpinnerService,
    private toastr: ToastrService,
    private modalService: NgbModal
  ) 
  {
    this.id = this.activatedRoute.snapshot.paramMap.get('id');

    if (this.id === undefined || this.id == '') {
      //this.router.navigate(['/']);
    }
    this.SpinnerService.show();
    this.apiService.getItem(+this.id).subscribe(
      data => {
        this.item = data;
        this.apiService.getSource(+this.id).subscribe(
          data => {
            this.source = data;
          }
        );
        this.apiService.getDerived(+this.id).subscribe(
          data => {
            this.derived = data;
          }
        );
        this.SpinnerService.hide();
      },
      error => {
        this.toastr.error(error.message, 'Error!');
        this.SpinnerService.hide();
      }
    );
    
    this.modalOptions = {
      backdrop:'static',
      backdropClass:'customBackdrop'
    }
  }

  ngOnInit() {
  }

  onUpdateName(id:number, name:string){
    window.scroll(0,0);
    this.SpinnerService.show();
    this.apiService.updateItemName(id, name).subscribe(
      data => {
        this.item = data;
        this.SpinnerService.hide();
      },
      error => {
        this.toastr.error(error.message, 'Error!');
        this.SpinnerService.hide();
      }
    );
  }

  onUpdateSource(id:number, source:number){
    window.scroll(0,0);
    this.SpinnerService.show();
    this.apiService.updateItemSource(id, source).subscribe(
      data => {
        this.item = data;this.apiService.getSource(+this.id).subscribe(
          data => {
            this.source = data;
          }
        );
        this.apiService.getDerived(+this.id).subscribe(
          data => {
            this.derived = data;
          }
        );
        this.SpinnerService.hide();
      },
      error => {
        this.toastr.error(error.message, 'Error!');
        this.SpinnerService.hide();
      }
    );
  }

  onAddLocation(id:number, place:string, description: string){
    window.scroll(0,0);
    this.SpinnerService.show();
    this.apiService.addLocation(id, place, description).subscribe(
      data => {
        this.item = data;
        this.SpinnerService.hide();
      },
      error => {
        this.toastr.error(error.message, 'Error!');
        this.SpinnerService.hide();
      }
    );
  }

  onUpdateLocation(id:number, position:number, place:string, description:string){
    if(place != ''){
      window.scroll(0,0);
      this.SpinnerService.show();
      this.apiService.updateItemLocation(id, position, place, description).subscribe(
        data => {
          this.item = data;
          this.SpinnerService.hide();
        },
        error => {
          this.toastr.error(error.message, 'Error!');
          this.SpinnerService.hide();
        }
      );
    }
  }

  onDeleteLocation(id:number){
    window.scroll(0,0);
    this.SpinnerService.show();
    this.apiService.deleteLastLocation(id).subscribe(
      data => {
        this.item = data;
        this.SpinnerService.hide();
      },
      error => {
        this.toastr.error(error.message, 'Error!');
        this.SpinnerService.hide();
      }
    );
  }

  open(content: any) {
    this.modalService.open(content, this.modalOptions).result.then((result) => {
      this.closeResult = `Closed with: ${result}`;
    }, (reason) => {
      
      this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
    });
  }

  private getDismissReason(reason: any): string {
    if (reason === ModalDismissReasons.ESC) {
      return 'by pressing ESC';
    } else if (reason === ModalDismissReasons.BACKDROP_CLICK) {
      return 'by clicking on a backdrop';
    } else {
      return `with: ${reason}`;
    }
  }
}
