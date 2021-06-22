import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AddItemComponent } from './components/addItem/addItem.component';
import { EditItemComponent } from './components/editItem/editItem.component';
import { ItemsComponent } from './components/items/items.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  {
    path: '',
    canActivate: [AuthGuard],
    component: ItemsComponent
  },
  {
    path: 'addItem',
    canActivate: [AuthGuard],
    component: AddItemComponent
  },
  {
    path: 'editItem/:id',
    canActivate: [AuthGuard],
    component: EditItemComponent
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'register/:id',
    canActivate: [AuthGuard],
    component: RegisterComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
