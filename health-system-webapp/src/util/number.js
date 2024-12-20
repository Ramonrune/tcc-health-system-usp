export const getOnlyNumbers = (str) => {
  if (typeof str === "string") {
    const numbers = str.match(/\d+/g);
    const result = numbers ? numbers.join("") : "";
    return result;
  }
  return "";
};
