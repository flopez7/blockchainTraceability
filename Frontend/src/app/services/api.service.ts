import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Item } from '../models/item';


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  url: string = 'http://localhost:5000/blockchain/'
  httpOptions = {
    headers:{
      'Content-Type': 'application/json'
    }
  };

  constructor(
    private httpClient: HttpClient,
    ) { }

  getItems():Observable<Item[]>{
    return this.httpClient.get<Item[]>(this.url+'getItems');
  }

  getItem(id:number):Observable<Item>{
    return this.httpClient.get<Item>(this.url+'getItem?id='+id);
  }

  getSource(id:number):Observable<Item>{
    return this.httpClient.get<Item>(this.url+'getSource?id='+id);
  }

  getDerived(id:number):Observable<Item[]>{
    return this.httpClient.get<Item[]>(this.url+'getDerived?id='+id);
  }

  addItem(name:string, place:string, description:string):Observable<Item>{
    const item = {
      name: name,
      place: place,
      description: description
    }
    return this.httpClient.post<Item>(this.url+'setItem', item, this.httpOptions);
  }

  addLocation(id:number, place:string, description:string):Observable<Item>{
    const item = {
      id: id,
      place: place,
      description: description
    }
    return this.httpClient.post<Item>(this.url+'setLocation', item, this.httpOptions);
  }

  updateItemName(id:number, name:string):Observable<Item>{
    const item = {
      id: id,
      name: name,
    }
    return this.httpClient.put<Item>(this.url+'updateItemName', item, this.httpOptions);
  }

  updateItemSource(id:number, source:number):Observable<Item>{
    const item = {
      id: id,
      source: source,
    }
    return this.httpClient.post<Item>(this.url+'setSource', item, this.httpOptions);
  }

  updateItemLocation(id:number, position:number, place:string, description:string):Observable<Item>{
    const item = {
      id: id,
      position:position,
      place: place,
      description: description
    }
    return this.httpClient.put<Item>(this.url+'updateLocation', item, this.httpOptions);
  }

  deleteItem(id:number):Observable<Item[]>{
    return this.httpClient.delete<Item[]>(this.url+'deleteItem?id='+id);
  }

  deleteLastLocation(id:number):Observable<Item>{
    return this.httpClient.delete<Item>(this.url+'deleteLastLocation?id='+id);
  }
}
