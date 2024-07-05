using Flexalon;
using UnityEngine;

public class DraggableHandler : MonoBehaviour
{
    // Ajoutez une référence au parent spécifique que vous souhaitez vérifier
    public Transform targetParent;

    void OnEnable()
    {
        // Vérifiez si le parent de l'objet correspond au parent cible
        if (IsInTargetParent(transform))
        {
            ActivateDraggableOnChildren();
        }
    }

    void OnDisable()
    {
        // Optionnel: Désactiver le draggable sur les enfants lorsque ce script est désactivé
        DeactivateDraggableOnChildren();
    }

    private void ActivateDraggableOnChildren()
    {
        FlexalonInteractable[] interactables = GetComponentsInChildren<FlexalonInteractable>();
        foreach (var interactable in interactables)
        {
            interactable.Draggable = true;
        }
    }

    private void DeactivateDraggableOnChildren()
    {
        FlexalonInteractable[] interactables = GetComponentsInChildren<FlexalonInteractable>();
        foreach (var interactable in interactables)
        {
            interactable.Draggable = false;
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