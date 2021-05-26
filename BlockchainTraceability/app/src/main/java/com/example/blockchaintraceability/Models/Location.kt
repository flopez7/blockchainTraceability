package com.example.blockchaintraceability.Models

import com.google.gson.annotations.SerializedName

data class Location(
    @SerializedName("place")
    var place: String,
    @SerializedName("description")
    var description: String,
    @SerializedName("datetime")
    var datetime: String
)