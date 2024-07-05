using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SnapController : MonoBehaviour
{
    public List<Transform> snapPoints;
    public List<Draggable> draggableObjects;
    public float snapRange = 0.5f;
    // Start is called before the first frame update
    void Start()
    {
        foreach(Draggable draggable in draggableObjects) { }
    }

    private void OnDragEnded(Draggable draggable)
    {
        float closestDistance = -1;
        Transform closestSnapPoint = null;

        foreach (Transform snapPoint in snapPoints)
        {
            float currentDistance = Vector2.Distance(draggable.transform.localPosition, snapPoint.localPosition);
            if(closestSnapPoint == null|| currentDistance < closestDistance)
            {
                closestSnapPoint = snapPoint;
                closestDistance = currentDistance;
            }
        }
        if(closestSnapPoint != null && closestDistance<= snapRange) {
            draggable.transform.localPosition = closestSnapPoint.localPosition;

        }
    }
}
