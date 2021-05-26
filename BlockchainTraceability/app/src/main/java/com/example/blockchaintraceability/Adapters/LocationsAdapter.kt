package com.example.blockchaintraceability.Adapters

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.blockchaintraceability.Models.Location
import com.example.blockchaintraceability.R

class LocationsAdapter: RecyclerView.Adapter<LocationsAdapter.ViewHolder>() {

    var locations: List<Location> = ArrayList()
    lateinit var context: Context

    fun LocationsAdapter(locations: List<Location>, context: Context) {
        this.locations = locations
        this.context = context
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        return ViewHolder(layoutInflater.inflate(R.layout.item_locations, parent,false))
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = locations.get(position)
        holder.bind(item, position)
    }

    override fun getItemCount(): Int {
        return locations.size
    }

    class ViewHolder (view: View) : RecyclerView.ViewHolder(view){
        private val location = view.findViewById(R.id.location) as TextView
        private val place = view.findViewById(R.id.place) as TextView
        private val description = view.findViewById(R.id.description) as TextView
        private val datetime = view.findViewById(R.id.datetime) as TextView

        fun bind(item: Location, position: Int) {
            location.text = "Location " + position + ": "
            place.text = "Place: " + item.place
            description.text = "Description: " + item.description
            datetime.text = "Time: " + item.datetime
        }
    }
}