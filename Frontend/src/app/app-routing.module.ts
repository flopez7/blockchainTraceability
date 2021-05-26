import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AddItemComponent } from './components/addItem/addItem.component';
import { EditItemComponent } from './components/editItem/editItem.component';
import { ItemsComponent } from './components/items/items.component';

const routes: Routes = [
  {
    path: '',
    component: ItemsComponent
  },
  {
    path: 'addItem',
    component: AddItemComponent
  },
  {
    path: 'editItem/:id',
    component: EditItemComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
