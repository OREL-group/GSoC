
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
public class CustomScrollRect:ScrollRect
{
    public override void OnBeginDrag(PointerEventData eventData)
{
    // Vérifie si le point de départ du glissement est sur la scrollbar
    if (IsPointerOverScrollbar(eventData))
    {
        base.OnBeginDrag(eventData);
    }
}

public override void OnDrag(PointerEventData eventData)
{
    // Vérifie si le point de glissement est sur la scrollbar
    if (IsPointerOverScrollbar(eventData))
    {
        base.OnDrag(eventData);
    }
}

public override void OnEndDrag(PointerEventData eventData)
{
    // Vérifie si le point de fin du glissement est sur la scrollbar
    if (IsPointerOverScrollbar(eventData))
    {
        base.OnEndDrag(eventData);
    }
}

private bool IsPointerOverScrollbar(PointerEventData eventData)
{
    // Vérifie si le pointer est sur la barre de défilement verticale ou horizontale
    if (verticalScrollbar != null)
    {
        if (RectTransformUtility.RectangleContainsScreenPoint(verticalScrollbar.GetComponent<RectTransform>(), eventData.position, eventData.pressEventCamera))
        {
            return true;
        }
    }

    if (horizontalScrollbar != null)
    {
        if (RectTransformUtility.RectangleContainsScreenPoint(horizontalScrollbar.GetComponent<RectTransform>(), eventData.position, eventData.pressEventCamera))
        {
            return true;
        }
    }

    return false;
}
}