using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Flexalon;

public class DragAndDropHandler : MonoBehaviour
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
        // Assurez-vous que FlexalonInteractable est attaché au GameObject
        FlexalonInteractable interactable = GetComponent<FlexalonInteractable>();
        interactable.DragStart.AddListener(OnDragStart);
        interactable.DragEnd.AddListener(OnDragEnd);
        // Sauvegarder la position originale dans la hiérarchie
        originalParent = transform.parent;
        originalSiblingIndex = transform.GetSiblingIndex();
        rootCanvas = GetComponentInParent<Canvas>().rootCanvas;
    }

    private void OnDragStart(FlexalonInteractable interactable)
    {
        if (EnableCopy)
        {
            // Détacher l'objet du parent pour le rendre draggable partout
            transform.SetParent(rootCanvas.transform, true);
        }
    }

    private void OnDragEnd(FlexalonInteractable interactable)
    {
        // Créer une copie de l'objet à la position actuelle
        if (EnableCopy)
        {
            // GameObject objectCopy = Instantiate(gameObject, transform.position, transform.rotation, rootCanvas.transform);
            GameObject objectCopy = Instantiate(gameObject, transform.position, transform.rotation);

            // Ajuster la taille et la position pour correspondre à l'objet original
            RectTransform originalRectTransform = GetComponent<RectTransform>();
            RectTransform copyRectTransform = objectCopy.GetComponent<RectTransform>();
            copyRectTransform.sizeDelta = originalRectTransform.sizeDelta;
            copyRectTransform.localScale = originalRectTransform.localScale;

            // Désactiver le script sur l'objet original pour éviter de multiples copies
            // objectCopy.GetComponent<DragAndDropHandler>().enabled = false;
            objectCopy.GetComponent<DragAndDropHandler>().enableCopy = false;

            // Assigner la copie à targetParent
            if (targetParent != null)
            {
                objectCopy.transform.SetParent(targetParent, false);
                objectCopy.transform.localPosition = Vector3.zero; // Assurez-vous que la copie est placée correctement
            }

            // Réinitialiser la position de l'objet original dans la hiérarchie
            transform.SetParent(originalParent);
            transform.SetSiblingIndex(originalSiblingIndex);
            transform.localPosition = Vector3.zero; // Assurez-vous que l'objet retourne à sa position relative originale

            // Réinitialiser la taille et la position de l'objet original
            // GetComponent<RectTransform>().sizeDelta = originalRectTransform.sizeDelta;
            // GetComponent<RectTransform>().localScale = originalRectTransform.localScale;
        }
        else
        {
            /*if (reorderable)
            {
                ActivateDraggableOnChildren(this.gameObject);
            }*/
            // Vérifier si c'est dans target component ou original parent sinon supprimer l'objet
            if (!IsInTargetParent(transform) || !IsInTargetParent(targetParent))
            {
                Destroy(gameObject);
            }
        }
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
