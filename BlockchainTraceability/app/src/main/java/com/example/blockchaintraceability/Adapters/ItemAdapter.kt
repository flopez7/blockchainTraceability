package com.example.blockchaintraceability.Adapters

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.blockchaintraceability.Models.Item
import com.example.blockchaintraceability.R

class ItemAdapter : RecyclerView.Adapter<ItemAdapter.ViewHolder>() {

    var items: MutableList<Item>  = mutableListOf()
    lateinit var context: Context

    fun ItemAdapter(items: MutableList<Item>, context: Context){
        this.items = items
        this.context = context
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = items.get(position)
        holder.bind(item, context)
    }

    override fun getItemViewType(position: Int): Int {
        return items[position].type
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        if (viewType != 0)
            return ViewHolder(layoutInflater.inflate(R.layout.card_item, parent, false))
        else
            return ViewHolder(layoutInflater.inflate(R.layout.content_item, parent, false))
    }

    override fun getItemCount(): Int {
        return items.size
    }
    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        private val itemId = view.findViewById(R.id.itemId) as TextView
        private val itemName = view.findViewById(R.id.itemName) as TextView?
        private val itemLocation = view.findViewById(R.id.itemLocation) as TextView?
        private val recyclerView = view.findViewById(R.id.recyclerView) as RecyclerView?
        private val itemConnected = view.findViewById(R.id.titleConnected) as TextView?

        fun bind(item: Item, context: Context) {
            itemId.text = "Id: " + item.id.toString()
            if (itemName != null) {
                itemName.text = item.name
            }
            if (itemLocation != null) {
                itemLocation.text = "Location: " + item.locations[item.locations.count()-1].place + " (" + item.locations[item.locations.count()-1].datetime + ")"
            }
            if (recyclerView != null) {
                setRecyclerView(item,context)
            }
            if (itemConnected != null) {
                setTitleItem(item)
            }
        }

        fun setRecyclerView(item: Item,context: Context) {
            val mAdapter = LocationsAdapter()
            recyclerView?.setHasFixedSize(true)
            recyclerView?.layoutManager = LinearLayoutManager(context)
            mAdapter.LocationsAdapter(item.locations, context)
            recyclerView?.adapter = mAdapter
        }

        fun setTitleItem(item: Item) {
            when (item.type) {
                1 -> {
                    itemConnected?.visibility = View.VISIBLE
                    itemConnected?.text = "Source"
                }
                2 -> {
                    itemConnected?.visibility = View.VISIBLE
                    itemConnected?.text = "Derived"
                }
                else -> itemConnected?.visibility = View.GONE
            }
        }
    }
}