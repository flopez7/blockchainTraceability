package com.example.blockchaintraceability.Services

import com.example.blockchaintraceability.Models.Item
import com.example.blockchaintraceability.Models.SendLocation
import com.example.blockchaintraceability.Objects.RetrofitClient
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ApiService {
    fun getItem(id: Int, onResult: (Item?) -> Unit){
        RetrofitClient.INSTANCE.getItem(id).enqueue(
            object : Callback<Item> {
                override fun onFailure(call: Call<Item>, t: Throwable) {
                    onResult(null)
                }
                override fun onResponse( call: Call<Item>, response: Response<Item>) {
                    onResult(response.body())
                }
            }
        )
    }

    fun getSource(id: Int, onResult: (Item?) -> Unit){
        RetrofitClient.INSTANCE.getSource(id).enqueue(
            object : Callback<Item> {
                override fun onFailure(call: Call<Item>, t: Throwable) {
                    onResult(null)
                }
                override fun onResponse( call: Call<Item>, response: Response<Item>) {
                    onResult(response.body())
                }
            }
        )
    }

    fun getDerived(id: Int, onResult: (List<Item>?) -> Unit){
        RetrofitClient.INSTANCE.getDerived(id).enqueue(
            object : Callback<List<Item>> {
                override fun onFailure(call: Call<List<Item>>, t: Throwable) {
                    onResult(null)
                }
                override fun onResponse( call: Call<List<Item>>, response: Response<List<Item>>) {
                    onResult(response.body())
                }
            }
        )
    }

    fun sendLocation(sendLocation: SendLocation, onResult: (Item?) -> Unit){
        RetrofitClient.INSTANCE.sendLocation(sendLocation).enqueue(
            object : Callback<Item> {
                override fun onFailure(call: Call<Item>, t: Throwable) {
                    onResult(null)
                }
                override fun onResponse( call: Call<Item>, response: Response<Item>) {
                    onResult(response.body())
                }
            }
        )
    }

}