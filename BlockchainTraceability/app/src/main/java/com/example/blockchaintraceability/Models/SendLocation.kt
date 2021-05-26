package com.example.blockchaintraceability.Models

import com.google.gson.annotations.SerializedName

data class SendLocation(
    @SerializedName("id")
    var id: Number,
    @SerializedName("place")
    var place: String,
    @SerializedName("description")
    var description: String
)