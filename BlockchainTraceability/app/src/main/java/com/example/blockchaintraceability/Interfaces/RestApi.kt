package com.example.blockchaintraceability.Interfaces

import com.example.blockchaintraceability.Models.Item
import com.example.blockchaintraceability.Models.SendLocation
import retrofit2.Call
import retrofit2.http.*

interface RestApi {
    @GET("getItem")
    fun getItem(@Query("id") id: Int): Call<Item>
    @GET("getItems")
    fun getItems(): Call<List<Item>>
    @GET("getSource")
    fun getSource(@Query("id") id: Int): Call<Item>
    @GET("getDerived")
    fun getDerived(@Query("id") id: Int): Call<List<Item>>
    @POST("setLocation")
    fun sendLocation(@Body sendLocation: SendLocation):Call<Item>
}