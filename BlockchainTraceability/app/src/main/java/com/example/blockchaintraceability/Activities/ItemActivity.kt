package com.example.blockchaintraceability.Activities

import android.app.Dialog
import android.content.DialogInterface
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.blockchaintraceability.Adapters.ItemAdapter
import com.example.blockchaintraceability.Models.Item
import com.example.blockchaintraceability.Models.SendLocation
import com.example.blockchaintraceability.R
import com.example.blockchaintraceability.Services.ApiService
import com.google.android.material.floatingactionbutton.FloatingActionButton
import kotlinx.android.synthetic.main.activity_item.*

class ItemActivity : AppCompatActivity(), AddNewLocationDialogFragment.LocationDialogListener {
    private val apiService = ApiService()
    lateinit var mRecyclerView : RecyclerView
    val mAdapter : ItemAdapter = ItemAdapter()
    var itemId : Int = 0
    lateinit var item : Item
    var source : Item? = null
    var derived : List<Item>? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_item)
        setSupportActionBar(findViewById(R.id.toolbar))
        custom_overlay_view.visibility = View.VISIBLE

        val message = intent.getStringExtra("id")
        if(message == null){
            custom_error_view.visibility = View.VISIBLE
            custom_overlay_view.visibility = View.GONE
            supportActionBar?.setDisplayHomeAsUpEnabled(true)
            supportActionBar?.setDisplayShowHomeEnabled(true)
            Toast.makeText(this, "Error al obtener identificador", Toast.LENGTH_LONG).show()
        }
        else{
            itemId = message.toInt()
            getItemData(itemId)
        }

        findViewById<FloatingActionButton>(R.id.addLocation).setOnClickListener {
            val dialog = AddNewLocationDialogFragment()
            dialog.show(supportFragmentManager, "AddNewLocationDialogFragment")
        }

    }

    fun getItemData(itemId: Int){
        apiService.getItem(itemId){
            if (it != null) {
                item = it

                apiService.getSource(itemId){
                    source = it

                    apiService.getDerived(itemId){
                        derived = it
                        custom_overlay_view.visibility = View.GONE
                        title = item.name
                        supportActionBar?.setDisplayHomeAsUpEnabled(true)
                        supportActionBar?.setDisplayShowHomeEnabled(true)
                        val items = getListItem(item,source,derived)
                        setUpRecyclerView(items)
                    }
                }
            } else {
                custom_error_view.visibility = View.VISIBLE
                custom_overlay_view.visibility = View.GONE
                supportActionBar?.setDisplayHomeAsUpEnabled(true)
                supportActionBar?.setDisplayShowHomeEnabled(true)
                Toast.makeText(this, "Error al obtener el Item "+ itemId.toString(), Toast.LENGTH_LONG).show()
            }
        }
    }

    fun setUpRecyclerView(items: MutableList<Item>){
        mRecyclerView = findViewById<RecyclerView>(R.id.rvItem)
        mRecyclerView.setHasFixedSize(true)
        mRecyclerView.layoutManager = LinearLayoutManager(this)
        mAdapter.ItemAdapter(items, this)
        mRecyclerView.adapter = mAdapter
    }

    private fun getListItem(item: Item, source: Item?, derived: List<Item>?): MutableList<Item>{
        val listItems : MutableList<Item> = mutableListOf()
        item.type=0
        listItems.add(item)

        if(source != null){
            source.type=1
            listItems.add(source)
        }

        if(derived != null){
            derived.forEach { x->
                if (x == derived[0])
                    x.type = 2
                else
                    x.type = 3
            }
            listItems.addAll(derived)
        }

        return listItems
    }

    override fun onDialogPositiveClick(dialog: DialogInterface) {
        val f = dialog as Dialog
        val place = f.findViewById<View>(R.id.place) as EditText
        val description = f.findViewById<View>(R.id.description) as EditText
        if (place.text.isNullOrEmpty() || description.text.isNullOrEmpty()){
            Toast.makeText(this, "Debe completar los campos", Toast.LENGTH_LONG).show()
            return
        }
        val newLocation = SendLocation(itemId,place.text.toString(),description.text.toString())

        custom_overlay_view.visibility = View.VISIBLE
        apiService.sendLocation(newLocation){
            custom_overlay_view.visibility = View.GONE
            if (it != null) {
                item = it
                val items = getListItem(item,source,derived)
                setUpRecyclerView(items)
            } else {
                Toast.makeText(this, "Error al enviar nueva localizacion", Toast.LENGTH_LONG).show()
            }
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return true
    }
}