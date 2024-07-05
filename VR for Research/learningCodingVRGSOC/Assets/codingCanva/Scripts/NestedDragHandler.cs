using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Flexalon;

public class NestedDragHandler : MonoBehaviour
{
    private Transform originalParent;
    private int originalSiblingIndex;
    private Canvas rootCanvas;
    private bool enableCopy = true;
    public Transform targetParent;
    public bool EnableCopy { get => enableCopy; set => enableCopy = value; }
    public bool reorderable = true;

    void Start()
    {
        FlexalonInteractable interactable = GetComponent<FlexalonInteractable>();
        interactable.DragStart.AddListener(OnDragStart);
        interactable.DragEnd.AddListener(OnDragEnd);

        originalParent = transform.parent;
        originalSiblingIndex = transform.GetSiblingIndex();
        rootCanvas = GetComponentInParent<Canvas>().rootCanvas;
    }

    private void OnDragStart(FlexalonInteractable interactable)
    {
        if (EnableCopy)
        {
            transform.SetParent(rootCanvas.transform, true);
        }
    }

    private void OnDragEnd(FlexalonInteractable interactable)
    {
        if (EnableCopy)
        {
            GameObject objectCopy = Instantiate(gameObject, transform.position, transform.rotation);
            RectTransform originalRectTransform = GetComponent<RectTransform>();
            RectTransform copyRectTransform = objectCopy.GetComponent<RectTransform>();
            copyRectTransform.sizeDelta = originalRectTransform.sizeDelta;
            copyRectTransform.localScale = originalRectTransform.localScale;

            objectCopy.GetComponent<NestedDragHandler>().enableCopy = false;

            Transform targetChild = GetTargetChildUnderMouse();
            if (targetChild != null)
            {
                objectCopy.transform.SetParent(targetChild, false);
                objectCopy.transform.localPosition = Vector3.zero;
            }

            transform.SetParent(originalParent);
            transform.SetSiblingIndex(originalSiblingIndex);
            transform.localPosition = Vector3.zero;
        }
        else
        {
            if (reorderable)
            {
                ActivateDraggableOnChildren(this.gameObject);
            }

            if (!IsInTargetParent(transform) || !IsInTargetParent(targetParent))
            {
                Destroy(gameObject);
            }
        }
    }

    private Transform GetTargetChildUnderMouse()
    {
        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        RaycastHit hit;

        if (Physics.Raycast(ray, out hit))
        {
            Transform hitTransform = hit.transform;
            while (hitTransform != null)
            {
                if (hitTransform.parent == targetParent)
                {
                    return hitTransform;
                }
                hitTransform = hitTransform.parent;
            }
        }
        return null;
    }

    private void ActivateDraggableOnChildren(GameObject parentObject)
    {
        if (IsInTargetParent(parentObject.transform))
        {
            FlexalonInteractable[] interactables = parentObject.GetComponentsInChildren<FlexalonInteractable>();
            foreach (var interactable in interactables)
            {
                interactable.Draggable = true;
            }
        }
    }

    private bool IsInTargetParent(Transform transform)
    {
        Transform current = transform;
        while (current != null)
        {
            if (current == targetParent)
            {
                return true;
            }
            current = current.parent;
        }
        return false;
    }
}
