import {
  parse,
  format,
  differenceInYears,
  parseISO,
  subMonths,
} from "date-fns";

export const convertDate = (
  inputDate,
  from = "dd/MM/yyyy",
  to = "yyyy-MM-dd"
) => {
  const parsedDate = parse(inputDate, from, new Date());

  const formattedDate = format(parsedDate, to);

  return formattedDate;
};

export const calculateAge = (inputDate) => {
  const birthDate = parseISO(inputDate);
  const age = differenceInYears(new Date(), birthDate);
  return age;
};

export const getToday = () => {
  return format(new Date(), "yyyy-MM-dd");
};

export const getDateMinusMonth = (month) => {
  return format(subMonths(new Date(), month), "MMM");
};
