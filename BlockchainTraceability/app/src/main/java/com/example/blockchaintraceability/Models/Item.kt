package com.example.blockchaintraceability.Models

import com.google.gson.annotations.SerializedName

data class Item(
    @SerializedName("id")
    var id: Number,
    @SerializedName("name")
    var name: String,
    @SerializedName("source")
    var source: Number,
    @SerializedName("locations")
    var locations: List<Location>,
    var type: Int
)