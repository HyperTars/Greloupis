function ErrorPage(errCode) {
  if (errCode["errCode"] === "403") window.location.href = "/403";
  else if (errCode["errCode"] === "404") window.location.href = "/404";
  else if (errCode["errCode"].startsWith("50")) window.location.href = "/500";

  return;
}

export default ErrorPage;
