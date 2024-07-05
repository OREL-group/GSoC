using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GoOut : MonoBehaviour
{
    private void Start()
    {
        GetComponent<Trigger_Zone>().onEnterEvent.AddListener(InsideTrash);
    }
    public void wentOut(GameObject go) { go.SetActive(false); }
    public void InsideTrash(GameObject go) { go.SetActive(false);}
}
