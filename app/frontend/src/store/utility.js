export const updateObject = (oldObject, updatedProperties) => {
    return {
        ...oldObject, // ... creates a clone of the oldObject
        ...updatedProperties // replace oldObject with the updatedProperties
    }
}