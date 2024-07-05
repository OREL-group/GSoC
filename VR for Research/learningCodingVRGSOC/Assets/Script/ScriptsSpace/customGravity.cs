using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class CustomGravity : MonoBehaviour
{
    private Rigidbody rb;
    public float gravityMagnitude = 9.81f;  // Gravité standard

    void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    void FixedUpdate()
    {
        // Applique une force de gravité vers le "bas" du vaisseau
        Vector3 gravityDirection = -transform.up;  // Adapte cette direction selon la configuration de ton vaisseau
        rb.AddForce(gravityDirection * gravityMagnitude * rb.mass);
    }
}