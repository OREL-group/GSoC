using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class Trigger_Zone : MonoBehaviour
{
    public string targertTag;
    public UnityEvent<GameObject> onEnterEvent;
    private void OnTriggerEnter(Collider other)
    {
        onEnterEvent.Invoke(other.gameObject);
    }
}
