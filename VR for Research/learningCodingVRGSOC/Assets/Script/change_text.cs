using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class change_text : MonoBehaviour
{
    public GameObject text_ini;
    public GameObject text_congrats;


    // Start is called before the first frame update
    void Start()
    {
        //text_mesh = GetComponentInChildren<TextMesh>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnCollisionEnter(Collision collision)
    {
        Debug.Log("!!!!! OnCollisionrEnter");
        if (collision.collider.CompareTag("tag_book") ) {
            Destroy(text_ini);
            text_congrats.transform.localScale = new Vector3(1f, 1f, 1f);
            Debug.Log("!!!!!OnCollisionrEnter - tag_shell");
        }

    } 
}
