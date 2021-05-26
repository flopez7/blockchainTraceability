package com.example.blockchaintraceability.Activities

import android.app.Dialog
import android.content.Context
import android.content.DialogInterface
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.widget.EditText
import androidx.appcompat.app.AlertDialog
import androidx.fragment.app.DialogFragment
import com.example.blockchaintraceability.R


class AddNewLocationDialogFragment : DialogFragment() {

    internal lateinit var listener: LocationDialogListener

    interface LocationDialogListener {
        fun onDialogPositiveClick(dialog: DialogInterface)
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        try {
            listener = context as LocationDialogListener
        } catch (e: ClassCastException) {
            // The activity doesn't implement the interface, throw exception
            throw ClassCastException((context.toString() +
                    " must implement LocationDialogListener"))
        }
    }

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        return activity?.let {
            val factory = LayoutInflater.from(context)
            val view: View = factory.inflate(R.layout.dialog_location, null)
            val builder = AlertDialog.Builder(it)
            // Get the layout inflater
            val inflater = requireActivity().layoutInflater
            val placeText = view.findViewById<EditText>(R.id.place)
            val descriptionText = view.findViewById<EditText>(R.id.description)

            // Inflate and set the layout for the dialog
            // Pass null as the parent view because its going in the dialog layout
            builder.setView(inflater.inflate(R.layout.dialog_location, null))
                // Add action buttons
                .setPositiveButton("Add",
                    DialogInterface.OnClickListener { dialog, _ ->

                        listener.onDialogPositiveClick(dialog)
                    })
                .setNegativeButton("Cancel",
                    DialogInterface.OnClickListener { dialog, id ->
                        getDialog()?.cancel()
                    })
            val dialog = builder.create()
            dialog
        } ?: throw IllegalStateException("Activity cannot be null")
    }
}