package com.example.blockchaintraceability.Objects

import com.example.blockchaintraceability.Interfaces.RestApi
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient {
    private const val BASE_URL : String = "https://78dc22d267f1.ngrok.io/blockchain/"
    private val loggin = HttpLoggingInterceptor().apply { setLevel(HttpLoggingInterceptor.Level.BODY) }
    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor() { chain ->
            val original = chain.request()

            val requestBuilder = original.newBuilder()
                .method(original.method, original.body)

            val request = requestBuilder.build()
            chain.proceed(request)
        }
        .addInterceptor(loggin)
        .build()

    val INSTANCE : RestApi by lazy{
        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .client(okHttpClient)
            .build()
        retrofit.create(RestApi::class.java)
    }
}
